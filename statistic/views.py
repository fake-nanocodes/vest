from django.shortcuts import render,redirect
from utils import  can_access_dashboard
from .models import Statistic
from .forms import StatisticForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/accounts/login')
@can_access_dashboard
def dashboard_statistic(request):
    statistic, created = Statistic.objects.get_or_create(id=1)
    form = StatisticForm(instance=statistic)
   
    context = {
        'form':form, 
    }
    if request.method == 'POST':
        form = StatisticForm(request.POST,instance=statistic)
        if form.is_valid():
            form.save()
            messages.success(request,'A new statistic was created')
        else:
            messages.error(request,'There was an error with your request')
    return render(request,'dashboard/setting5.html',context)


def dashboard_delete_statistic(request,pk):
    statistic = Statistic.objects.get(id=pk)
    statistic.delete()
    return redirect('/statistic/dashboard')