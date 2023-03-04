from .models import User
from django import forms
from django.contrib.auth import authenticate
from phonenumber_field.formfields import PhoneNumberField

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email','phone_number','address','city','state','pincode')

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("phone_number", )
