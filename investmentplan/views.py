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
#smail
from notification.models import Notification
from plan.models import Plan
from .forms import InvestmentPlanForm
# Create your views here.
@login_required(login_url='/accounts/login')
@check_profile_exists
def user_plan(request):
    plans = InvestmentPlan.objects.all()
    categories = Category.objects.all()
    profile = Profile.objects.get(user=request.user)
    context = {
        'plans':plans,
        'profile':profile,
        'categories':categories,
    }
    if request.method == 'POST':
        amount = request.POST.get('amount')
        plan_name = request.POST.get('plan_name')
        try:
            # print(plan_name)
            # print(InvestmentPlan.objects.all())
            investmentplan = InvestmentPlan.objects.get(name=plan_name)
        except InvestmentPlan.DoesNotExist:
            messages.error(request, 'There was an error with your investment')
            return render(request,'user/plans.html',context)
        if amount == '' or amount == None:
            messages.error(request, 'Your investment was invalid')
            return render(request,'user/plans.html',context)
        if int(float(amount)) > investmentplan.maximum_amount + 1:
            messages.error(request, 'Your investment amount exceeded the allowed amount')
            return render(request,'user/plans.html',context)
        if int(float(amount)) > investmentplan.maximum_amount + 1:
            messages.error(request, 'Your investment amount exceeded the allowed amount')
            return render(request,'user/plans.html',context)
        if int(float(amount)) < investmentplan.minimum_amount - 1:
            messages.error(request, 'Your investment amount is lower than the the allowed amount')
            return render(request,'user/plans.html',context)
        if int(float(amount)) > profile.available_balance:
            messages.error(request, 'You do not have enough funds')
            return render(request,'user/plans.html',context)
        try:
            profile.available_balance -= float(amount) 
            profile.save()
            profit = (int(float(amount)) * investmentplan.investment_profit_percent)/100
            plan_history = InvestmentPlanHistory.objects.create(profile=profile,investmentplan=investmentplan,amount=amount,profit=profit)
            plan_history.save()
            plan_cal = Plan.objects.create(profile=profile,investmentplan=investmentplan,amount=amount,profit=profit)
            plan_cal.save()
            
            try:
                referral = Referral.objects.get(user=request.user)
                referralPrice = (investmentplan.referral_profit_percent * int(float(amount)))/100
                referral.referral_profit += referralPrice
                referral.user.profile.available_balance += referralPrice
                referral.user.profile.save()
                referral.save()  
                try:
                    email_thread = threading.Thread(target=send_email,args=("Referral Gain",f'Your referral gain is {referralPrice} from {request.user.username}',referral.user.profile.user.email))
                    email_thread.start()
                except Exception as e:
                    print(e)      
                
            except Exception as e:
                print(e)
            messages.success(request, 'You have applied for the ' + plan_name + ' plan ')
            notification = Notification.objects.create(profile=profile, action=f'{plan_name.upper()}', description=f'You have successfully applied for the {plan_name} plan')
            notification.save()
            if request.user.email:
                try:
                    email_thread = threading.Thread(target=send_email,args=(plan_name,f'You have applied for the {plan_name} plan ',request.user.email))
                    email_thread.start()
                except Exception as e:
                    print(e)
                
        except Exception as e:
            messages.error(request,'There was an error without your request')
            print(e)
        return redirect('/plans')
        
    return render(request,'user/plans.html',context)


@login_required(login_url='/accounts/login')
@check_profile_exists
def user_plan_history(request):
    profile = Profile.objects.get(user=request.user)
    plans = InvestmentPlanHistory.objects.filter(profile=profile)
    context = {
        'plans': plans,
        'profile':profile,
    }
    return render(request,'user/plan_history.html',context)

@login_required(login_url='/accounts/login')
@can_access_dashboard
def dashboard_investment_plan(request):
    form = InvestmentPlanForm()
    investmentplan = InvestmentPlan.objects.all()
    context = {
        'form':form,
      'plans':investmentplan  
    }
    if request.method == 'POST':
        form = InvestmentPlanForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'A new investment plan was created')
        else:
            messages.error(request,'There was an error with your request')
    return render(request,'dashboard/setting.html',context)

@login_required(login_url='/accounts/login')
@can_access_dashboard
def dashboard_delete_investment_plan(request,pk):
    plan = InvestmentPlan.objects.get(id=pk)
    plan.delete()
    return redirect('/plans/dashboard')