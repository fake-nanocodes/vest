from django.db import models
from datetime import timedelta,date
from userprofile.models import Profile
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class InvestmentPlan(models.Model):
    name = models.CharField(max_length=50,null=True,blank=True,unique=True)
    minimum_amount = models.IntegerField(default=0,null=True,blank=True)
    maximum_amount = models.IntegerField(default=0,null=True,blank=True)
    number_of_days = models.IntegerField(default=0,null=True,blank=True)
    investment_profit_percent = models.FloatField(default=0,null=True,blank=True)
    referral_profit_percent = models.FloatField(default=0,null=True,blank=True)
    created = models.DateField(auto_now_add=True,null=True,blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-created']
        verbose_name ='InvestmentPlan'  
        verbose_name_plural ='InvestmentPlan'  
        
    def __str__(self):
        return self.name


class InvestmentPlanHistory(models.Model):
    investmentplan = models.ForeignKey(InvestmentPlan,on_delete=models.CASCADE,related_name='plan')
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='profile')
    amount = models.DecimalField(max_digits=20,decimal_places=5,blank=True,null=True)
    profit = models.DecimalField(max_digits=20,decimal_places=5,blank=True,null=True)
    created = models.DateField(auto_now_add=True,null=True,blank=True)
    
    class Meta:
        ordering = ['-created']
        verbose_name ='InvestmentPlanHistory'  
        verbose_name_plural ='InvestmentPlanHistory'    
        
    def __str__(self):
        return f'  plan'
    
    def stillRunning(self):
        status = ''
        
        
        plan_end_date = self.created + timedelta(days=self.investmentplan.number_of_days)
    
        time_difference_days = plan_end_date - date.today()
        time_difference = time_difference_days.days
    
        if time_difference > 0:
            status = 'Still Running'
        else:
            status = 'Done'
        return status 
    
    def get_maturity_date(self):
        plan_end_date = self.created + timedelta(days=self.investmentplan.number_of_days)
        return plan_end_date
    
# class Plan(models.Model):
#     profile = models.ForeignKey(Profile,on_delete=models.CASCADE,blank=True)
#     number_of_days = models.IntegerField(default=0,null=True,blank=True)
#     investment_profit_percent = models.FloatField(default=0,null=True,blank=True)
#     referral_profit_percent = models.FloatField(default=0,null=True,blank=True)
#     amount = models.IntegerField(default=0,null=True,blank=True)
#     profit = models.FloatField(default=0,null=True,blank=True)
#     created = models.DateField(auto_now_add=True,null=True,blank=True)
    
#     def __str__(self):
#         return f'{self.profile.user.username}'
    
#     def stillRunning(self):
#         status = ''
        
        
#         plan_end_date = self.date_created + timedelta(days=self.number_of_days)
    
#         time_difference_days = plan_end_date - date.today()
#         time_difference = time_difference_days.days
    
#         if time_difference > 0:
#             status = 'Still Running'
#         else:
#             status = 'Done'
#         return status 
    
#     def get_maturity_date(self):
#         plan_end_date = self.date_created + timedelta(days=self.number_of_days)
#         return plan_end_date