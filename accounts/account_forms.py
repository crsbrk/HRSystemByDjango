from django import forms
from django.contrib.auth.models import User
from .models import UserProfileInfo

class UserForm(forms.ModelForm):
    #password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control'}))

    class Meta():
        model = User
        fields = ('password','email')
        # widgets = {
        #     'username': forms.TextInput(
		# 		attrs={
		# 			'class': 'form-control'
		# 			}
		# 		),
        #     'email': forms.EmailInput(
		# 		attrs={
		# 			'class': 'form-control'
		# 			}
		# 		),
        #     'passsword':forms.PasswordInput(
        #         attrs={
		# 			'class': 'form-control'
		# 			}
		# 		),
            
            
		# 	}

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('profile_phone','profile_pic','profile_site','profile_descption')

        # widgets = {
        #     'profile_phone': forms.NumberInput(
		# 		attrs={
		# 			'class': 'form-control'
		# 			}
		# 		),
        #     'profile_site': forms.URLInput(
		# 		attrs={
		# 			'class': 'form-control'
		# 			}
		# 		),
        #     'profile_descption': forms.Textarea(
		# 		attrs={
		# 			'class': 'form-control'
		# 			}
		# 		),
        #     'profile_pic': forms.FileInput(
		# 		attrs={
		# 			'class': 'form-control custom-file'
		# 			}
		# 		),
		# 	}