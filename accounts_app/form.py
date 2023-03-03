from .models import User
from django import forms
from django.contrib.auth import authenticate
from phonenumber_field.formfields import PhoneNumberField
from otp.fields import OTPField

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email','phone_number','address','city','state','pincode')

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("phone_number", )

class CustomLoginForm(forms.Form):
    phone_number = PhoneNumberField()
    otp = OTPField()

    def clean(self):
        cleaned_data = super().clean()
        phone_number = cleaned_data.get('phone_number')
        otp = cleaned_data.get('otp')
        
        if phone_number and otp:
            user = authenticate(phone_number=phone_number, otp=otp)
            if user is None:
                raise forms.ValidationError('Invalid mobile number or OTP')
        return cleaned_data