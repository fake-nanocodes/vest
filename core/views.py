from django.shortcuts import render
from investmentplan.models import  InvestmentPlan

# Create your views here.

def about(request):
    
    return render(request,'about.html')
                
def banner(request):
    
    return render(request,'banner.html')
                
def contact(request):
    
    return render(request,'contact.html')
                
def faq(request):
   
    return render(request,'faq.html')
                
                
def index(request):
    
    plans = InvestmentPlan.objects.all()
    context ={
        'plans':plans
    }
    return render(request,'index.html',context)
                
                
def payment(request):
 
    return render(request,'payment.html')
                
def plans(request):
    
    plans = InvestmentPlan.objects.all()
    context ={
        'plans':plans
    }
    return render(request,'plans.html',context)
                
                
def terms(request):
    
    return render(request,'terms.html')
                #views created