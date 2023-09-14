from django import forms
from .models import *


            
class StatisticForm(forms.ModelForm):
    class Meta:
        model = Statistic
        fields = '__all__'
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})