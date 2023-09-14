from django import forms
from .models import *


            
class ProfileBalanceForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['available_balance']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['loginemailblocked']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})