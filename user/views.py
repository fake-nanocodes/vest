from django.shortcuts import render,redirect
from utils import  can_access_dashboard
from django.contrib.auth import get_user_model
User = get_user_model()
from userprofile.models import Profile
from .models import *
from userprofile.decorators import check_profile_exists
from referral.models import Referral
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import threading
from utils import send_email
from decimal import Decimal
#smail
from django.conf import settings
from transaction.models import Transaction
from django.db.models import Sum
from website.forms import WebsiteForm
from walletaddress.forms import WalletAddressForm
from website.models import Website
from walletaddress.models import WalletAddress
from deposit.models import Deposit
from withdraw.models import Withdrawal
from deposit.forms import DepositForm
from withdraw.forms import WithdrawalForm
from bonus.models import Bonus
from datetime import timedelta
from django.utils import timezone
from investmentplan.forms import InvestmentPlanHistoryForm
from investmentplan.models import InvestmentPlan, InvestmentPlanHistory
from userprofile.forms import ProfileBalanceForm, ProfileForm
from .forms import UserForm
from plan.models import Plan
# Create your views here.

@login_required(login_url='/accounts/login')
@check_profile_exists
def user_dashboard(request):
    profile = Profile.objects.get(user=request.user)
    transactions = Transaction.objects.filter(profile=profile)[:5]
    referrals = Referral.objects.filter(user=request.user)
    referrals_profit = referrals.aggregate(total_referral_profit=Sum('referral_profit'))['total_referral_profit']
    
    plans = Plan.objects.filter(profile=profile)
    active_plans = [plan for plan in plans if plan.stillRunning == True]
    
    
    current_datetime = timezone.now()
    
    profile.live_profit = 0
    if active_plans:
        profile.book_balance = profile.available_balance
    else:
        profile.book_balance = 0
    profile.save()
    
    for plan in plans:
        if plan.stillRunning == True:
            profit_per_day = plan.profit / Decimal(plan.investmentplan.number_of_days)
            
            days_passed = (current_datetime - plan.created).days + 1
            
            profit_earned_day = profit_per_day * Decimal(days_passed)
            
            plan.profile.book_balance += (float(plan.profit) + plan.amount)
            plan.profile.live_profit += float(profit_earned_day)
            print(plan.profile.book_balance)
            print(plan.profile.live_profit)
          
            plan.profile.save()
    
    for plan in plans:
        if plan.stillRunning == False:
            plan.profile.available_balance += (float(plan.profit) + plan.amount)
            print(float(plan.profit) + plan.amount)
            print(plan.profile.available_balance)
            try:
                plan.profile.save()
                plan.save()
                plan.delete()
            except Exception as e:
                print(e)
    context = {
        'profile':profile,
        'transactions':transactions,
        'referrals':referrals,
         'referrals_profit':referrals_profit,
    }
    return render(request,'user/index.html',context)


@login_required(login_url='/accounts/login')
@can_access_dashboard
def admin_dashboard(request):
    walletInstance, created = WalletAddress.objects.get_or_create(id=1)
    websiteInstance, created = Website.objects.get_or_create(id=1)
    if request.method == 'POST':
        websiteForm = WebsiteForm(request.POST,instance=websiteInstance)
        walletForm = WalletAddressForm(request.POST,instance=walletInstance)

        if websiteForm.is_valid() and walletForm.is_valid():
            websiteForm_instance = websiteForm.save()

            walletForm_instance = walletForm.save()

            return redirect('/user/dashboard')
    
    else:  
        walletInstance, created = WalletAddress.objects.get_or_create(id=1)
        websiteInstance, created = Website.objects.get_or_create(id=1)
        websiteForm = WebsiteForm(instance=websiteInstance)
        walletForm = WalletAddressForm(instance=walletInstance)
        total_users = User.objects.all().count()
        deposit = Deposit.objects.all()
        withdrawal = Withdrawal.objects.all()
        deposit_model = deposit.filter(verified=True).aggregate(Sum('usdt_amount'))
        total_deposit = deposit_model['usdt_amount__sum'] or 0
        
        withdrawal_model = withdrawal.filter(verified=True).aggregate(Sum('usdt_amount'))
        total_withdrawal = withdrawal_model['usdt_amount__sum'] or 0
        
        total_balance = float(total_deposit) - float(total_withdrawal)
        
        unverified_deposit = deposit.filter(verified=False).aggregate(Sum('usdt_amount'))
        total_unverified_deposit = unverified_deposit['usdt_amount__sum'] or 0

        unverified_withdrawal = withdrawal.filter(verified=False).aggregate(Sum('usdt_amount'))
        total_unverified_withdrawal = unverified_withdrawal['usdt_amount__sum'] or 0

        bonus = Bonus.objects.all().aggregate(Sum('usdt_amount'))
        total_bonus = bonus['usdt_amount__sum'] or 0
        
        twenty_four = timezone.now()  - timedelta(days=1)
        seven_days = timezone.now()  - timedelta(days=7)
        thirty_days = timezone.now()  - timedelta(days=30)
        one_year = timezone.now()  - timedelta(days=365)
        
        twenty_four_in = (deposit.filter(created__gte=twenty_four).aggregate(Sum('usdt_amount'))['usdt_amount__sum']) or 0
        seven_days_in = (deposit.filter(created__gte=seven_days).aggregate(Sum('usdt_amount'))['usdt_amount__sum']) or 0
        thirty_days_in = (deposit.filter(created__gte=thirty_days).aggregate(Sum('usdt_amount'))['usdt_amount__sum']) or 0
        one_year_in = (deposit.filter(created__gte=one_year).aggregate(Sum('usdt_amount'))['usdt_amount__sum']) or 0
        
        twenty_four_out = (withdrawal.filter(created__lte=twenty_four).aggregate(Sum('usdt_amount'))['usdt_amount__sum']) or 0 
        seven_days_out = (withdrawal.filter(created__lte=seven_days).aggregate(Sum('usdt_amount'))['usdt_amount__sum']) or 0 
        thirty_days_out = (withdrawal.filter(created__lte=thirty_days).aggregate(Sum('usdt_amount'))['usdt_amount__sum']) or 0 
        one_year_out = (withdrawal.filter(created__lte=one_year).aggregate(Sum('usdt_amount'))['usdt_amount__sum']) or 0 
        
        twenty_four_balance = round((twenty_four_in - twenty_four_out),2)
        seven_days_balance = round((seven_days_in - seven_days_out),2)
        thirty_days_balance = round((thirty_days_in - thirty_days_out),2)
        one_year_balance = round((one_year_in - one_year_out),2)
        context = {
            'walletForm':walletForm,
            'websiteForm':websiteForm,
            'total_deposit': round(total_deposit,2),
        'total_withdrawal': round(total_withdrawal,2),
        'total_balance': round(total_balance,2),
        'total_users': total_users,
            'total_unverified_deposit':round(total_unverified_deposit,2),
        'total_unverified_withdrawal': round(total_unverified_withdrawal,2),
        'total_bonus': round(total_bonus,2),
        'twenty_four_in':round(twenty_four_in,2) ,
        'seven_days_in':round(seven_days_in,2) ,
        'thirty_days_in':round(thirty_days_in,2) ,
        'one_year_in':round(one_year_in,2) ,
        'twenty_four_out':round(twenty_four_out,2) ,
        'seven_days_out':round(seven_days_out,2) ,
        'thirty_days_out':round(thirty_days_out,2) ,
        'one_year_out':round(one_year_out,2) ,
        'twenty_four_balance':round(twenty_four_balance,2) ,
        'seven_days_balance':round(seven_days_balance,2) ,
        'thirty_days_balance':round(thirty_days_balance,2) ,
        'one_year_balance':round(one_year_balance,2) ,
            }
    return render(request,'dashboard/index.html',context)

@login_required(login_url='/accounts/login')
@can_access_dashboard
def admin_dashboard_user(request):
    profiles = Profile.objects.all()
    context = {
        'profiles':profiles,
       
    }
    return render(request,'dashboard/users.html',context)

@login_required(login_url='/accounts/login')
@can_access_dashboard
def delete_user(request,pk):
    profile = Profile.objects.get(id=pk)
    user = User.objects.get(id=profile.user.id)
    user.delete()
    
    return redirect('/user/dashboard/users')

@login_required(login_url='/accounts/login')
@can_access_dashboard
def admin_add_user_deposit(request,pk):
    profile = Profile.objects.get(id=pk)
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            try:
                formInstance = form.save(commit=False)
                formInstance.profile = profile
                formInstance.verified = True
                formInstance.save()
                transaction = Transaction.objects.create(profile=profile, transaction_type='deposit', usdt_amount=formInstance.usdt_amount, description=f'Your deposit of {formInstance.amount} {formInstance.wallet_type} into {formInstance.wallet_address} is verified',verified=True)
                transaction.save()
                messages.success(request, f'You have deposited {formInstance.amount} {formInstance.wallet_type} into {formInstance.wallet_address} for the user {request.user.username}' )
            except Exception as e:
                print(e)
        else:
            print(form.errors)
            messages.error(request,'There was an error with your request')
    return redirect(f'/user/dashboard/user/{pk}')

@login_required(login_url='/accounts/login')
@can_access_dashboard
def editbalance(request,pk):
    profile = Profile.objects.get(id=pk)
    if request.method == 'POST':
        prevbalance = profile.available_balance
        form = ProfileBalanceForm(request.POST,instance=profile)
        if form.is_valid():
            form.save()
            messages.info(request, f'You have changed the user-{request.user.username}s available balance from {prevbalance} to {profile.available_balance}' )
        else:
            messages.error(request,'There was an error with your request')
    return redirect(f'/user/dashboard/user/{pk}')  
        
   
@login_required(login_url='/accounts/login')
@can_access_dashboard
def admin_add_user_withdrawal(request,pk):
    profile = Profile.objects.get(id=pk)
    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            formInstance = form.save(commit=False)
            amount = formInstance.usdt_amount
            print(amount)
            if amount > profile.available_balance:
                messages.error(request, f'The user-{request.user.username} has insufficient funds')
                return redirect(f'/user/dashboard/user/{pk}')
            formInstance.verified = True
            formInstance.profile = profile
            formInstance.save()
            transaction = Transaction.objects.create(profile=profile, transaction_type='withdrawal', usdt_amount=formInstance.usdt_amount, description=f'Your deposit of {formInstance.amount} {formInstance.wallet_type} into {formInstance.wallet_address} is verified',verified=True)
            transaction.save()
            messages.success(request, f'You have withdrawn {formInstance.amount} {formInstance.wallet_type} into {formInstance.wallet_address} for the user {request.user.username}' )
        else:
            messages.error(request,'There was an error with your request')
    return redirect(f'/user/dashboard/user/{pk}')

@login_required(login_url='/accounts/login')
@can_access_dashboard
def user_password_reset_by_admin(request,pk):
    if request.method == 'POST':
        password1 = request.POST['newpassword']
        password2 = request.POST['cnewpassword']
        
        if password1 != password2:
            messages.info(request,'The passwords did not match ')
            return redirect(f'/user/dashboard/user/{pk}')
        elif len(password1) <=  8 or len(password2) <=  8:
            messages.info(request,'The password was too short')
            return redirect(f'/user/dashboard/user/{pk}')
        try:
            user = User.objects.get(id=pk)
            user.set_password(password1)
            user.save()
            messages.info(request,'The password was set successfully')
        except:
            messages.info(request,'The password was not successfully')
        return redirect(f'/user/dashboard/user/{pk}')
 
@login_required(login_url='/accounts/login')
@can_access_dashboard   
def admin_make_investment_for_user(request,pk):
    profile = Profile.objects.get(id=pk)
    if request.method == 'POST':
        form = InvestmentPlanHistoryForm(request.POST)
        if form.is_valid():
            formInstance = form.save(commit=False)
            formInstance.profile = profile
            try:
                plan = InvestmentPlan.objects.get(name=formInstance.investmentplan.name)
            except InvestmentPlan.DoesNotExist:
                messages.error(request, 'There was an error with your investment')
                return redirect(f'/user/dashboard/user/{pk}')
            if formInstance.amount == '' or formInstance.amount == None:
                messages.error(request, 'Your investment was invalid')
                return redirect(f'/user/dashboard/user/{pk}')
            if int(float(formInstance.amount)) > plan.maximum_amount + 1:
                messages.error(request, 'Your investment amount exceeded the allowed amount')
                return redirect(f'/user/dashboard/user/{pk}')
            if int(float(formInstance.amount)) > plan.maximum_amount + 1:
                messages.error(request, 'Your investment amount exceeded the allowed amount')
                return redirect(f'/user/dashboard/user/{pk}')
            if int(float(formInstance.amount)) < plan.minimum_amount - 1:
                messages.error(request, 'Your investment amount is lower than the the allowed amount')
                return redirect(f'/user/dashboard/user/{pk}')
            if int(float(formInstance.amount)) > profile.available_balance:
                messages.error(request, 'You do not have enough funds')
                return redirect(f'/user/dashboard/user/{pk}')
            profile.available_balance -= float(formInstance.amount) 
            profile.save()
            profit = (int(float(formInstance.amount)) * plan.investment_profit_percent)/100
            formInstance.profit = profit
            formInstance.save()
            plan_cal = Plan.objects.create(profile=profile,investmentplan=plan,amount=formInstance.amount,profit=profit)
            plan_cal.save()
            
            try:
                referral = Referral.objects.get(referred_user=request.user)
                referralPrice = (plan.referral_profit_percent * int(float(formInstance.amount)))/100
                referral.referral_profit += referralPrice
                referral.user.profile.available_balance += referralPrice
                referral.user.profile.save()
                referral.save()        
                #send_email_task.delay("Referral Gain",f'Your referral gain is {referralPrice} from {request.user.username}',user_profile.user.email)
            except Exception as e:
                print(e)
            messages.info(request, 'You have applied for the ' + plan.name + ' plan ')
    return redirect(f'/user/dashboard/user/{pk}')

@login_required(login_url='/accounts/login')
@can_access_dashboard
def user_profile_update_by_admin(request,pk):
    profile = Profile.objects.get(id=pk)
    if request.method == 'POST':
        prevusername = request.user.username
        userform = UserForm(request.POST,instance=profile.user)
        profileform = ProfileForm(request.POST,instance=profile)
        
        if userform.is_valid() and profileform.is_valid():
            userinstance = userform.save()
            profileinstance = profileform.save()
            
        referrals = Referral.objects.filter(user__username=prevusername)
        
        for instance in referrals:
            instance.user.username = userinstance.username
            instance.save()
        
        messages.info(request, f"You have changed the user details")
        
    return redirect(f'/user/dashboard/user/{pk}')

@login_required(login_url='/accounts/login')
@can_access_dashboard
def admin_dashboard_user_detail(request,pk):
    profile = Profile.objects.get(id=pk)
    depositform = DepositForm()
    withdrawalform = WithdrawalForm()
    investmentplanhistoryform = InvestmentPlanHistoryForm()
    profilebalanceform = ProfileBalanceForm(instance=profile)
    plan_history = InvestmentPlanHistory.objects.filter(profile=profile)
    referrals = Referral.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(profile=profile)
    userform = UserForm(instance=profile.user)
    profileform = ProfileForm(instance=profile)
    
    bonuses = Bonus.objects.filter(profile=profile).aggregate(Sum('usdt_amount'))
    total_bonuses = bonuses['usdt_amount__sum'] or 0
    
    deposits = Deposit.objects.filter(profile=profile).aggregate(Sum('usdt_amount'))
    total_deposits = deposits['usdt_amount__sum'] or 0
    
    withdrawals = Withdrawal.objects.filter(profile=profile).aggregate(Sum('usdt_amount'))
    total_withdrawals = withdrawals['usdt_amount__sum'] or 0
    
    try:
        referred_by = Referral.objects.get(referred_user=profile.user)
    except Exception as e:
        referred_by = None
        print(e)
    
    context = {
         'depositform':depositform,
        'withdrawalform':withdrawalform,
        'profile':profile,
        'investmentplanhistoryform':investmentplanhistoryform,
        'transactions':transactions,
        'plan_history' :plan_history,
        'referrals':referrals,
        'profilebalanceform':profilebalanceform,
        'profileform':profileform,
        'userform':userform,
         'total_deposits': round(total_deposits,2),
        'total_withdrawals': round(total_withdrawals,2),
        'total_bonuses': round(total_bonuses,2),
        'referred_by':referred_by,
    }  
    return render(request,'dashboard/user.html',context)

def my_custom_error_view(request):
    return render(request,'other/error.html')

def my_custom_page_not_found_view(request,exception):
    return render(request,'other/error.html')


def my_custom_bad_request_view(request,exception):
    return render(request,'other/error.html')


def my_custom_permission_denied_view(request,exception):
    return render(request,'other/error.html')
