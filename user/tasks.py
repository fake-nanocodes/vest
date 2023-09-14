# from utils.util import send_email
from utils import send_email
from plan.models import Plan
from userprofile.models import Profile
import datetime
from datetime import timedelta,date
from django.utils import timezone
from decimal import Decimal

def plan_profit():
    plans = Plan.objects.all()
    profiles = Profile.objects.all()
    
   
    active_plans = [plan for plan in plans if plan.stillRunning == True]
    
    
    current_datetime = timezone.now()
    
    for profile in profiles:
        profile.live_profit = 0
        if active_plans:
            profile.book_balance = profile.available_balance
        else:
            profile.book_balance = 0
        profile.save()
        
    for plan in plans:
        if plan.stillRunning == True:
            profit_per_day = plan.profit / Decimal(plan.investmentplan.number_of_days)
            
            days_passed = (current_datetime - plan.created).days + 1
            
            profit_earned_day = profit_per_day * Decimal(days_passed)
            
            plan.profile.book_balance += (float(plan.profit) + plan.amount)
            plan.profile.live_profit += float(profit_earned_day)
            print(plan.profile.book_balance)
            print(plan.profile.live_profit)
          
            plan.profile.save()
    
    for plan in plans:
        if plan.stillRunning == False:
            plan.profile.available_balance += (float(plan.profit) + plan.amount)
            print(float(plan.profit) + plan.amount)
            print(plan.profile.available_balance)
            try:
                plan.profile.save()
                plan.save()
                plan.delete()
            except Exception as e:
                print(e)
                print(f"Error saving profile for plan {plan.id}: {str(e)}")
       
    return "Done with the plans"

"""@shared_task
def plan_profit():
    plans = Plan.objects.all()
    profiles = Profile.objects.all()
    
    print(plans)
    current_datetime = timezone.now()
    
    for profile in profiles:
        profile.live_profit = 0
        
        if plans.filter(stillRunning=True).exists():
            profile.book_balance = profile.available_balance
        else:
            profile.book_balance = 0
        
        profile.save()
        
    for plan in plans:
        profit_per_day = plan.profit / Decimal(plan.investmentplan.number_of_days)
        
        days_passed = (current_datetime - plan.created).days + 1
        
        profit_earned_day = profit_per_day * Decimal(days_passed)
        
        plan.profile.book_balance += (float(plan.profit) + plan.amount)
        plan.profile.live_profit += float(profit_earned_day)
        print(plan.profile.book_balance)
        print(plan.profile.live_profit)
      
        plan.profile.save()
        
        if not plan.stillRunning:
            plan.profile.available_balance += (float(plan.profit) + plan.amount)
            print(float(plan.profit) + plan.amount)
            print(plan.profile.available_balance)
            
            try:
                plan.profile.save()
                plan.delete()
            except Exception as e:
                print(e)
                print(f"Error saving profile or deleting plan {plan.id}: {str(e)}")
       
    return "Done with the plans"
"""
