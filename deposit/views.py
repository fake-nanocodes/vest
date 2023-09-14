from django.shortcuts import render,redirect
from utils import  can_access_dashboard
from django.contrib.auth import get_user_model
User = get_user_model()
from userprofile.models import Profile
from .models import Deposit
from userprofile.decorators import check_profile_exists
from walletaddress.models import WalletAddress
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from transaction.models import Transaction
import threading
from utils import send_email

from django.conf import settings
from notification.models import Notification
# Create your views here.




@login_required(login_url='/accounts/login')
@check_profile_exists
def user_deposit(request):
    profile = Profile.objects.get(user=request.user)
    deposits = Deposit.objects.filter(profile=profile).order_by('-created')[:5]
    wallet, _ =WalletAddress.objects.get_or_create(pk=1)
    
    context = {
        'wallet':wallet,
        'deposits': deposits,
        'profile':profile, 
    }
 

    if request.method == 'POST':
        wallet_address = request.POST['wallet_address']
        amount = request.POST['amount']
        wallet_type = request.POST['wallet_type']
        usdt_amount = request.POST['usdt_amount']
        
        print(wallet_type)
        deposit = Deposit.objects.create(profile=profile,amount=amount,wallet_type=wallet_type,wallet_address=wallet_address,usdt_amount=usdt_amount)
        deposit.save()
        print(deposit.wallet_type)
        action = f'Your deposit of {deposit.amount} {deposit.wallet_type} into {deposit.wallet_address} is pending'
        notification = Notification.objects.create(profile=profile, action='Deposit Pending', description=action)
        notification.save()
        transaction = Transaction.objects.create(profile=profile, transaction_type='deposit', usdt_amount=usdt_amount, description=action)
        transaction.save()
        
        try:
            email_thread = threading.Thread(target=send_email,args=('Deposit Requested',f'{profile.user.username} has deposited {deposit.amount} {deposit.wallet_type} into {deposit.wallet_address}', settings.RECIPIENT_ADDRESS)        )
            email_thread2 = threading.Thread(target=send_email,args=('Deposit Requested', f'Your deposit of {amount} {wallet_type} into {wallet_address} is pending', request.user.email)        )
            email_thread.start()
            email_thread2.start()
        except Exception as e:
            print(e)
        messages.info(request, 'You have applied for a deposit')
        return redirect('/deposit')
        
    return render(request,'user/deposit.html',context)

def verify(request,id):
    deposit = Deposit.objects.get(id=id)
    if deposit.verified == False:
        deposit.profile.available_balance += int(float(deposit.usdt_amount))
        deposit.profile.save()
        deposit.verified = True
        deposit.save()
    return redirect(request.META.get('HTTP_REFERER', '/admin'))

@login_required(login_url='/accounts/login')
@can_access_dashboard
def dashboard_deposit(request):
    deposits = Deposit.objects.all()
    
    context = {
        'deposits':deposits,
    }
    return render(request,'dashboard/deposit.html',context)

@login_required(login_url='/accounts/login')
@can_access_dashboard
def dashboard_deposit_completed(request):
    deposits = Deposit.objects.filter(verified=True)
    
    context = {
        'deposits':deposits,
    }
    return render(request,'dashboard/deposit3.html',context)

@login_required(login_url='/accounts/login')
@can_access_dashboard
def dashboard_deposit_pending(request):
    deposits = Deposit.objects.filter(verified=False)
    
    context = {
        'deposits':deposits,
    }
    return render(request,'dashboard/deposit4.html',context)

@login_required(login_url='/accounts/login')
@can_access_dashboard
def delete_deposit(request,id):
    deposit = Deposit.objects.get(id=id)
    deposit.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url='/accounts/login')
@check_profile_exists
def user_deposit_completed(request):
    profile = Profile.objects.get(user=request.user)
    deposits = Deposit.objects.filter(profile=profile,verified=True)
    
    
    context = {
        'deposits':deposits,
    }
    return render(request,'user/completeddeposit.html',context)

@login_required(login_url='/accounts/login')
@check_profile_exists
def user_deposit_pending(request):
    profile = Profile.objects.get(user=request.user)
    deposits = Deposit.objects.filter(profile=profile,verified=False)
    
    
    context = {
        'deposits':deposits,
    }
    return render(request,'user/pendingdeposit.html',context)
