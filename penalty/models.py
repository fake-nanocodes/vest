from django.db import models
from userprofile.models import Profile
# Create your models here.

class Penalty(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    usdt_amount = models.FloatField(default=0,null=True,blank=True)
    action = models.TextField(blank=True,null=True)
    seen = models.BooleanField(default=False)
    user_see = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
   
    class Meta:
        verbose_name = 'Penalty'
        verbose_name_plural = 'Penalties'
        ordering = ['-created']
        
    def __str__(self):
        return f'{self.profile.user.username} has been givn a penalty of {self.usdt_amount}'