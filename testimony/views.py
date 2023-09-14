from django.shortcuts import render,redirect
from utils import  can_access_dashboard
from .models import Testimony
from .forms import TestimonyForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/accounts/login')
@can_access_dashboard
def dashboard_testimony(request):
    form = TestimonyForm()
    testimonies = Testimony.objects.all()
    context = {
        'form':form,
      'testimonies':testimonies  
    }
    if request.method == 'POST':
        form = TestimonyForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'A new testimony was created')
        else:
            messages.error(request,'There was an error with your request')
    return render(request,'dashboard/setting2.html',context)

@login_required(login_url='/accounts/login')
@can_access_dashboard
def dashboard_delete_testimony(request,pk):
    testimony = Testimony.objects.get(id=pk)
    testimony.delete()
    return redirect('/testimony/dashboard')