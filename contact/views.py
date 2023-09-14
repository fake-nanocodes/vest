from django.shortcuts import render,redirect
from utils import  can_access_dashboard
from django.contrib.auth import get_user_model
User = get_user_model()
from userprofile.models import Profile
from userprofile.decorators import check_profile_exists
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import threading
from utils import send_email
#smail
from django.conf import settings
# Create your views here.

@login_required(login_url='/accounts/login')
@check_profile_exists
def user_contact(request): 
    profile = Profile.objects.get(user=request.user)
    context = {
        'profile':profile,
        
    }
    if request.method == 'POST':
        body = request.POST.get('body')
        subject = request.POST.get('subject')
        try:
            email_thread = threading.Thread(target=send_email,args=(subject,body,settings.RECIPIENT_ADDRESS))
            email_thread.start()
            messages.success(request, 'Your email has been sent')
        except Exception as e:
            messages.error(request, 'There was an error with your request')
            print(e)
        
        return redirect('/contact')
    return render(request,'user/support.html',context)

@login_required(login_url='/accounts/login')
@can_access_dashboard
def dashboard_contact(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']
        recipient = list(User.objects.values_list('email', flat=True))  
        recipient_list = [email for email in recipient if email != None]
        print(recipient_list)
        try:
            for email in recipient_list:
                email_thread = threading.Thread(target=send_email,args=(subject,message,email))
                email_thread.start()
            messages.success(request, 'Your emails has been sent')
        except Exception as e:
            messages.error(request, 'There was an error with your request')
            print(e)
        
    return render(request,'dashboard/msg2.html')

@login_required(login_url='/accounts/login')
@can_access_dashboard
def dashboard_contact_user(request,pk):
    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']
        recipient = Profile.objects.get(id=pk)
        try:
            email_thread = threading.Thread(target=send_email,args=(subject,message,recipient.user.email))
            email_thread.start()
            
            messages.success(request, 'Your email has been sent')
        except Exception as e:
            messages.error(request, 'There was an error with your request')
            print(e)
        
    return render(request,'dashboard/msg2.html')

