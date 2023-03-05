from django.shortcuts import render
from django.views.generic import CreateView
from django.views import View 
from .form import SignUpForm,LoginForm,OTPForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView,FormView
from accounts_app.models import User
from blooddrop.utils import send_sms
from django import forms
from datetime import datetime
from random import choice
import string
from django.conf import settings


# Create your views here.
class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = '/user/sign-in/'

# For the demo
class VerifyOtpView(CreateView):
    form_class = OTPForm
    success_url = '/dashboard/'
    template_name = 'verify_otp.html'

class IndexView(View):
    def get(self):
        return HttpResponse('you have login successfully')
    
class LoginView(CreateView):
    model = User
    template_name = "login.html"
    form_class = LoginForm
    success_url = '/user/signup/'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            user = self.model.objects.filter(phone_number=phone_number).first()
            if not user:
                raise forms.ValidationError({"phone_number" : "The user is not exists with this phone number"})
            
            generated_otp = ''.join(choice(string.digits) for _ in range(4))
            sms_message = "Hello dear customer,\nThis message from Blood drop for OTP code.\nYour OTP is :- {}.\nThanks for using Blood drop.".format(generated_otp)

            otp = None

            if settings.IS_FAST_SMS_SERVICE and int(settings.IS_FAST_SMS_SERVICE):
                sent_otp_response = send_sms([phone_number, ], sms_message)
                if not sent_otp_response.get("return"):
                    raise forms.ValidationError({"phone_number" : "Given phone number is wrong."})
            else:
                otp = 1234

            user.otp = otp
            user.otp_create_at = datetime.today()
            user.save()

            return redirect('verify-otp')
        return self.form_invalid(form)

