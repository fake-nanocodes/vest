from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
    
    loginemailblocked = forms.BooleanField(required=False)