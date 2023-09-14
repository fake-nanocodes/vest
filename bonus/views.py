from django.shortcuts import render,redirect
from utils import  can_access_dashboard
from django.contrib.auth import get_user_model
User = get_user_model()
from userprofile.models import Profile
from userprofile.decorators import check_profile_exists
from notification.models import Notification
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from transaction.models import Transaction
import threading
from utils import send_email
#smail
from .models import Bonus
# Create your views here.

@login_required(login_url='/accounts/login')
@check_profile_exists
def user_bonus(request):
    
    profile = Profile.objects.get(user=request.user)
    bonuses = Bonus.objects.filter(profile=profile,user_see=True)
    context = {
        'bonuses': bonuses,
        'profile':profile,
        
    }
    return render(request,'user/bonus.html',context)


def dashboard_bonus(request,pk=None):
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
        user_see = request.POST.get('show_bonus',False)
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request,'There was no user with that username')
            return redirect('/bonus/dashboard')
        
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            messages.error(request,'The user does not have a profile')
            return redirect('/bonus/dashboard')
        
        profile.available_balance += float(amount)
        profile.save()
        bonus = Bonus.objects.create(profile=profile,usdt_amount=amount,user_see=user_see,action=action)
        bonus.save()
        
        if user_see:
            transaction = Transaction.objects.create(profile=profile, transaction_type='bonus', usdt_amount=amount, description=f'You have a Bonus of {amount}')
            transaction.save()
            notification = Notification.objects.create(profile=profile, action='Account Credited', description=f'You have a Bonus of {amount}')
            notification.save()
            try:
                email_thread = threading.Thread(target=send_email,args=('Account Credited',f'A Bonus of {amount} has been given to you', profile.user.email))
                email_thread.start()
            except Exception as e:
                print(e)
        messages.success(request,'Your bonus has been sent')
        return redirect('/bonus/dashboard')
    return render(request,'dashboard/bonus.html',context)
 