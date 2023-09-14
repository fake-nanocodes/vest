from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='userp')
    country = models.CharField(max_length=50,null=True,blank=True)
    image = models.ImageField(upload_to='profile_images', default='r.jpg')
    available_balance = models.FloatField(default=0)
    live_profit = models.FloatField(default=0)
    book_balance = models.FloatField(default=0)    
    loginemailblocked = models.BooleanField(blank=False,default=False)
    
    def __str__(self):
        return self.user.username 
    