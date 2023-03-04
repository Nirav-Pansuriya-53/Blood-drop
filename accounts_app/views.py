from django.shortcuts import render
from django.views.generic import CreateView
from .form import SignUpForm, LoginForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
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
    success_url = 'login/'
    

class LoginView(CreateView):
    model = User
    success_url = ""
    template_name = "login.html"
    form = LoginForm

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        form = self.form(data=request.data)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            user = self.model.objects.filter(phone_number=phone_number).first()
            if not user:
                raise forms.ValidationError({"phone_number" : "The user is not exists with this phone number"})
            
            generated_otp = ''.join(choice(string.digits) for _ in range(4))
            sms_message = "Hello dear customer,\nThis message from Blood drop for OTP code.\nYour OTP is :- {}.\nThanks for using Blood drop.".format(generated_otp)

            otp = None

            if int(settings.IS_FAST_SMS_SERVICE):
                sent_otp_response = send_sms([phone_number, ], sms_message)
                if not sent_otp_response.get("return"):
                    raise forms.ValidationError({"phone_number" : "Given phone number is wrong."})
            else:
                otp = 1234

            user.otp = otp
            user.otp_create_at = datetime.today()
            user.save()

            # below code use in verify otp
            # user = authenticate(request, phone_number=phone_number, otp=form.cleaned_data['otp'])
            # if user is not None:
            #     login(request, user)
            #     return redirect('home')

