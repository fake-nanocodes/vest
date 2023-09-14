from django.db import models

# Create your models here.
class Testimony( models.Model):
    name = models.CharField(blank=False,null=False,max_length=100)
    testimony = models.TextField(blank=False,null=False)
    image = models.ImageField(null=True,blank=True,upload_to="testimony")
    
    class Meta:
        verbose_name = "Testimony"
        verbose_name_plural = "Testimonies"
        
    def __str__(self):
         return f'{self.name} testimony has been created'