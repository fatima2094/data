from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.forms import ValidationError

from .models import code

class SignUpForm(UserCreationForm): 
    class Meta:
        model = User
        fields = settings.SIGN_UP_FIELDS
    username = forms.CharField(label='',max_length=30,min_length=5,required=True,widget=forms.TextInput(
			attrs={
				"placeholder": "Username",
				"class": "form-control"
			}
		)
	)
    email = forms.EmailField(label=(''), help_text=('Required. Enter an existing email address.'), widget=forms.TextInput(
			attrs={
				"placeholder": "Email",
				"class": "form-control"
			}
		))
	
    password1 = forms.CharField(
		label='',
		max_length=30,
		min_length=8,
		required=True,
		widget=forms.PasswordInput(
			attrs={
				"placeholder": "Password",
				"class": "form-control"
			}
		)
	)

    password2 = forms.CharField(
		label='',
		max_length=30,
		min_length=8,
		required=True,
		widget=forms.PasswordInput(
			attrs={
				"placeholder": "Confirm Password",
				"class": "form-control"
			}
		)
	)
    first_name = forms.CharField(label=(''),widget=forms.HiddenInput(),required=False,  max_length=200 )
    is_active = forms.BooleanField(label=(''),widget=forms.HiddenInput(),required=False)
    def clean_email(self):
        email = self.cleaned_data['email']

        user = User.objects.filter(email__iexact=email).exists()
        if user:
            raise ValidationError(('You can not use this email address.'))

        return email
class LoginForm(forms.ModelForm):
    '''Simple login form'''
    class Meta:
        model = User
        fields = ('username', 'password')



class OPTForm(forms.Form):
	OTP = forms.CharField(
		label='',
		max_length=254,
		widget=forms.TextInput(
			attrs={
				"placeholder": "OTP code",
				"class": "form-control"
			}
		)
	)