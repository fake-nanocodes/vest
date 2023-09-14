from django.db import models

# Create your models here.

class Statistic(models.Model):
    runingdays = models.IntegerField(null=True,blank=True,default=0)
    extradeposit = models.IntegerField(null=True,blank=True,default=0)
    extrawithdrawal = models.IntegerField(null=True,blank=True,default=0)
    extrausers = models.IntegerField(null=True,blank=True,default=0)
    
    def __str__(self):
        return "Extra stats"