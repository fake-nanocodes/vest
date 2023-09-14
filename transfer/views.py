from django.shortcuts import render,redirect
from utils import  can_access_dashboard
from django.contrib.auth import get_user_model
User = get_user_model()
from userprofile.models import Profile
from .models import Transfer
from userprofile.decorators import check_profile_exists
from walletaddress.models import WalletAddress
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from transaction.models import Transaction
import threading
from utils import send_email
#smail
from django.conf import settings
# Create your views here.
from django.db import transaction

@login_required(login_url='/accounts/login')
@check_profile_exists
@transaction.atomic
def user_transfer(request):
    if request.method == 'POST':
        try:
            email_address = request.POST.get('wallet_address')
            amount = float(request.POST.get('amount'))
            wallet_type = request.POST.get('wallet_type')
            usdt_amount = float(request.POST.get('usdt_amount'))
            
            user = request.user
            profile = user.profile
            
            if usdt_amount > profile.available_balance:
                messages.error(request, 'You have insufficient funds')
                return redirect('/transfer')
            
            try:
                transfer_user = User.objects.get(email=email_address)
                transfer_profile = transfer_user.profile
            except Exception as e:
                print(e)
                messages.error(request, 'There was an error with the user')
                return redirect('/transfer')
            
            with transaction.atomic():
                transfer = Transfer.objects.create(profile=profile,transfer_profile=transfer_profile, usdt_amount=usdt_amount)
                transfer_user = Transfer.objects.create(profile=profile,transfer_profile=transfer_profile, usdt_amount=usdt_amount, transferred=False)
                
                profile.available_balance -= usdt_amount
                profile.save()
                transfer_profile.available_balance += usdt_amount
                transfer_profile.save()
                
                Transaction.objects.create(profile=profile, transaction_type='transfer', usdt_amount=usdt_amount, description=f'You have transferred {usdt_amount} {wallet_type} to {transfer_profile.user.username}')
                Transaction.objects.create(profile=transfer_profile, transaction_type='transfer', usdt_amount=usdt_amount, description=f'{profile.user.username} has transferred {usdt_amount} {wallet_type} to you')
                
                # Assuming you have a function send_email_task
                
                try:
                    email_thread = threading.Thread(target=send_email,args=('Transfer', f'You have transferred {transfer.usdt_amount} USDT to {transfer_profile.user.email}', user.email))
                    email_thread.start()
                    email_thread2 = threading.Thread(target=send_email,args=('Transfer', f'{profile.user.username} has transferred {transfer.usdt_amount} USDT to {transfer_profile.user.email}', settings.RECIPIENT_ADDRESS))
                    email_thread2.start()
                    email_thread3 = threading.Thread(target=send_email,args=('Transfer', f'{profile.user.username} has transferred {transfer.usdt_amount} USDT to you', transfer_profile.user.email))
                    email_thread3.start()
                except Exception as e:
                    print(e)
                messages.success(request, 'You have made a transfer')
                return redirect('/transfer')
        except Exception as e:
            print(e)
            messages.error(request, 'There was an error with your transaction')
            return redirect('/transfer')
    
    # Move these lines outside of the POST request handling for efficiency
    user = request.user
    profile = user.profile
    transfers = Transfer.objects.filter(profile=profile).order_by('-created')[:5]
    
    context = {
        'profile': profile,
        'transfers': transfers,
    }
    
    return render(request, 'user/transfer.html', context)


