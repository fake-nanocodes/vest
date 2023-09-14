from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth import get_user_model
from referral.models import Referral 
User = get_user_model()

class CustomSignupForm(SignupForm):
    referral_code = forms.CharField(max_length=100, label='Referral Code',required=False)
    
 
    def save(self, request):
        user = super().save(request)
        try:
            user_refer = User.objects.get(username=self.cleaned_data['referral_code'])
            # print(user_refer)
            # print('iiiii')
            #referred user is the present user
            referral = Referral.objects.create(user=user_refer,referred_user=user)
            referral.save()
            return user
        except Exception as e:
            print(e)
            return user
        
        
        
# class CustomSignupForm(SignupForm):
#     referral_code = forms.CharField(max_length=100, label='Referral Code',required=False)
    
 
#     def save(self, request):
#         user = super().save(request)
#         try:
#             user_refer = User.objects.get(username=self.cleaned_data['referral_code'])
#             print(user_refer)
#         except User.DoesNotExist:
#             return user
#         try:
#             user.save()
#             # referred_user is the present user
#             referral = Referral.objects.create(referred_by=user_refer,referred_user=user.username)
#             referral.save()
#             return user
#         except Exception as e:
#             return userturn user
#         except Exception as e:
#             return user
        