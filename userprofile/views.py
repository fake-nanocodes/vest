from django.shortcuts import render,redirect
from utils import  can_access_dashboard
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Profile
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='/accounts/login')
def userprofile(request):
        
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None
       
    context = {
        'profile':profile,
    }
    
    if request.method == 'POST':    
        country = request.POST['country']
        image = request.FILES.get('image')
        
        profile, created = Profile.objects.get_or_create(user=request.user, defaults={'country': country, 'image': image})

        if not created:
            profile.country = country
            profile.image = image
            profile.save()
        
        return redirect('/user/')
        
    return render(request,'user/profile.html',context)