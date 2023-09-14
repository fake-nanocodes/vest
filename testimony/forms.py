from django import forms
from .models import *


            
class TestimonyForm(forms.ModelForm):
    class Meta:
        model = Testimony
        fields = '__all__'
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control','id':"getcatimage",'onchange':"displayImage(this,'#dispcatimage')",'style':"display:none;",'type':'file' })
        # <input class="form-control" id="getcatimage" value="" name="picimage" onchange="displayImage(this,'#dispcatimage')" style="display:none;" type="file">