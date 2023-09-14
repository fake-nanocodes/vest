from django.shortcuts import render,redirect
from utils import  can_access_dashboard
from django.contrib.auth import get_user_model
User = get_user_model()
from userprofile.models import Profile
from .models import Penalty
from userprofile.decorators import check_profile_exists
from walletaddress.models import WalletAddress
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from transaction.models import Transaction
import threading
from utils import send_email
#smail

# Create your views here.
@login_required(login_url='/accounts/login')
@check_profile_exists
def user_penalty(request):
    
    profile = Profile.objects.get(user=request.user)
    penalties = Penalty.objects.filter(profile=profile,user_see=True)
    context = {
        'penalties': penalties,
        'profile':profile,
        
    }
    return render(request,'user/penalty.html',context)   

@login_required(login_url='/accounts/login')
@can_access_dashboard
def dashboard_penalty(request,pk=None):
    if pk == None:
        users = User.objects.all()
        context = {
            'users':users,
                   'user':None
                   }
    else:
        user = User.objects.get(id=pk)
        context = {'user':user,
                   'users':None}
    
    if request.method == 'POST':
        username = request.POST.get('name')
        action = request.POST.get('action')
        amount = request.POST.get('amount')
        user_see = request.POST.get('show_penalty',False)
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request,'There was no user with that username')
            return redirect('/penalty/dashboard')
        
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            messages.error(request,'The user does not have a profile')
            return redirect('/penalty/dashboard')
        
        profile.available_balance += float(amount)
        profile.save()
        penalty = Penalty.objects.create(profile=profile,usdt_amount=amount,user_see=user_see,action=action)
        penalty.save()
        
        if user_see:
            transaction = Transaction.objects.create(profile=profile, transaction_type='penalty', usdt_amount=amount, description=action)
            transaction.save()
            try:
                email_thread = threading.Thread(target=send_email,args=('Account Debited',f'A Penalty of {amount} has been given to you',profile.user.email))
                email_thread.start()
            except Exception as e:
                print(e)
            
        messages.success(request,'Your penalty has been sent')
        return redirect('/penalty/dashboard')
    return render(request,'dashboard/bonus2.html',context)