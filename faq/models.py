from django.db import models

# Create your models here.

 
class FAQ( models.Model):
    question = models.CharField(blank=False,null=False,max_length=100)
    answer = models.TextField(blank=False,null=False)    
    
    class Meta:
        ordering=['-question']
    def __str__(self):
        return f'{self.question} question has been created'
