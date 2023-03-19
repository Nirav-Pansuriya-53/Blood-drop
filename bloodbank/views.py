from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, FormView
from django.views.generic import FormView
from bloodbank.models import BloodBank
# from django.contrib.auth.password_validation import validate_password
# from django.core.mail import send_mail
# from django.urls import reverse_lazy
# from blooddrop import settings
# from django.http import HttpResponseRedirect
# from django.urls import reverse
# import random
# import string
# from django.contrib.auth import authenticate, login
# from django.views import View
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth import authenticate

# Create your views here.

class IndexView(TemplateView):   
    template_name="bloodbank/index_bloodbank.html"

# class SignUpView(CreateView):
    # model = BloodBank
    # fields= ['email', 'address', 'city', 'state', 'pincode', ]
    # template_name ='bloodbank/signup_bloodbank.html'
    # success_url ='/bloodbank/index/'

    # def form_valid(self, form):
    #     # Generate a random password
    #     password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    #     # Set the password on the user instance
    #     BloodBank = form.save(commit=False)
    #     BloodBank.password = password
    #     BloodBank.save()

    #     # Send an email to the user with the password
    #     subject = 'Your Blood Bank account password'
    #     message = f'Your password is: {password}'
    #     from_email = settings.EMAIL_HOST_USER
    #     recipient_list = [BloodBank.email]
    #     send_mail(subject, message, from_email, recipient_list)

    #     return super().form_valid(form)

