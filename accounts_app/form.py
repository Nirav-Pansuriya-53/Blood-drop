from accounts_app.models import User,BloodGroup
from django import forms
import random
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

class SignUpForm(forms.ModelForm):
    group = forms.ChoiceField(choices=BloodGroup.BLOOD_GROUP_CHOICES)
    class Meta:
        model = User
        fields = ('name','email','phone_number','group','address','city','state','pincode')


    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        group = self.cleaned_data['group']
        if commit:
            user.save()
            BloodGroup.objects.create(user=user, blood_group=group)
        return user
    

class LoginForm(forms.Form):

    user = None
    email = forms.EmailField()

    def clean(self):
        email = self.cleaned_data.get('email')
        if email:
            user = User.objects.filter(email=email).first()
            if not user:
                raise forms.ValidationError({"email" : "User with this email is not exists"})
            
            otp = random.randint(100000, 999999)
            print(f"Email :- {user.email}", f"This is from Blood drop for OTP. Your OTP is :- {otp}")

            subject = 'Your OTP for logging in to our site'
            context = {"otp": otp, "user": user}
            message = render_to_string("user/otp_template.html", context)

            # Create the email message
            from_email = settings.EMAIL_HOST_USER
            to_email = [email]  # pass a list of email addresses
            otp_email = EmailMessage(subject, message, from_email, to_email)
            otp_email.content_subtype = "html"

            # Send the email
            otp_email.send()
           
            user.otp = otp 
            user.otp_created_at = datetime.today()
            user.save() 

            self.user = user
        return super().clean()

    def get_user(self):
        return self.user

  
class OTPForm(forms.Form):

    def __init__(self, user_id = None, *args, **kwargs):
        self.user_id = user_id
        self.user = None
        super().__init__(*args, **kwargs)

    otp = forms.IntegerField()

    def clean(self):
        otp = self.cleaned_data.get("otp",)
        if otp:
            user = User.objects.filter(id=self.user_id).first()

            if not user:
                raise forms.ValidationError({"otp" : "User is not found"})
            
            if user.otp != otp:
                raise forms.ValidationError({"otp" : "OTP is invalid, please try again with right one"})

            self.user = user
        return super().clean()
    
    def get_user(self):
        return self.user
