from django.db import models
from userprofile.models import Profile
from datetime import timedelta,date
from investmentplan.models import InvestmentPlan
from django.utils import timezone
# Create your models here.

class Plan(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True,blank=True)
    investmentplan = models.ForeignKey(InvestmentPlan,on_delete=models.CASCADE,related_name='investmentplan',null=True,blank=True)
    amount = models.FloatField(default=0,null=True,blank=True)
    profit = models.DecimalField(max_digits=20,decimal_places=5,blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return f'{self.profile.user.username}'
    
    @property #allow me to use it as an attribute
    def stillRunning(self):
        status = ''
        
        # Ensure both operands are of the same type (datetime)
        current_datetime = timezone.now()
        plan_end_datetime = self.created + timedelta(days=self.investmentplan.number_of_days)
    
        time_difference = plan_end_datetime - current_datetime
    
        if time_difference.total_seconds() > 0:
            status = True
        else:
            status = False
        return status
    
    def get_maturity_date(self):
        plan_end_date = self.created + timedelta(days=self.investmentplan.number_of_days)
        return plan_end_date
    