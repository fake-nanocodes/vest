from django.shortcuts import render,redirect
from utils import  can_access_dashboard
from .models import FAQ
from .forms import FAQForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/accounts/login')
@can_access_dashboard
def dashboard_faq(request):
    form = FAQForm()
    faqs = FAQ.objects.all()
    context = {
        'form':form,
      'faqs':faqs  
    }
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'A new faq was created')
        else:
            messages.error(request,'There was an error with your request')
    return render(request,'dashboard/setting3.html',context)

@login_required(login_url='/accounts/login')
@can_access_dashboard
def dashboard_delete_faq(request,pk):
    faq = FAQ.objects.get(id=pk)
    faq.delete()
    return redirect('/faq/dashboard')