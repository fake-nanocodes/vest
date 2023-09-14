from django.shortcuts import render,redirect
from utils import  can_access_dashboard
from django.contrib.auth import get_user_model
User = get_user_model()
from userprofile.models import Profile
from .models import Kyc
from userprofile.decorators import check_profile_exists
from notification.models import Notification
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from transaction.models import Transaction
from .forms import KycForm
# Create your views here.
#make and readonly and do like deposit verify
@login_required(login_url='/accounts/login')
@check_profile_exists
def user_kyc(request):
    
    try:
        user = User.objects.get(username=request.user.username)
        profile = Profile.objects.get(user=user)
        kyc = Kyc.objects.get(profile=profile)
        verified = kyc.verified
    except Kyc.DoesNotExist:
        kyc = None
        verified = False
    if kyc:
        form = KycForm(instance=kyc)
    else:
        form = KycForm()
    context= {
        'verified': verified,
        'profile':profile,
        'form':form
    }    
    if request.method == 'POST':
        if kyc:
            form = KycForm(request.POST,instance=kyc)
        else:
            form = KycForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            kyc_model = form.save(commit=False)
            kyc_model.profile=profile
            kyc_model.save()
            notification = Notification.objects.create(profile=profile, action='Kyc Submitted', description=f'You have successfully submitted your Kyc form')
            notification.save()
        
        messages.info(request, 'You have submitted your kyc details')
        return redirect('/kyc')
    
    return render(request,'user/kyc.html',context)

@login_required(login_url='/accounts/login')
@can_access_dashboard
def verify(request,id):
    profile = Profile.objects.get(user=request.user)
    kyc = Kyc.objects.get(id=id)
    if kyc.verified == False:
        kyc.verified = True
        kyc.save()
        notification = Notification.objects.create(profile=profile, action='Kyc Verified', description=f'Your Kyc form was verified')
        notification.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))