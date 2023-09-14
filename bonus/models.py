from django.db import models
from userprofile.models import Profile

# Create your models here.
class Bonus(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    usdt_amount = models.FloatField(default=0,null=True,blank=True)
    action = models.TextField(blank=True,null=True)
    seen = models.BooleanField(default=False)
    user_see = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    
    class Meta:
        verbose_name = 'Bonus'
        verbose_name_plural = 'Bonuses'
        ordering = ['-created']
        
    def __str__(self):
        return f'{self.profile.user.username} has been givn a bonus of {self.usdt_amount}'