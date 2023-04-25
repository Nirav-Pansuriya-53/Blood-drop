from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from bloodbank.models import BloodBank
from blooddrop import settings
import random
import string
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_save
from django.dispatch import receiver
from bloodbank.models import Donation

@receiver(post_save, sender=BloodBank)
def send_blood_bank_email(sender, instance, created, **kwargs):
    if created:
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        #BloodBank = form.save(commit=False)
        user = instance.user  # Get the related User instance
        user.password = make_password(password)  # Set the password on the User instance
        user.save()
        subject = 'Your BloodBank for logging in to our site'
        context = {"password": password, "user":instance.user.email}
        message = render_to_string("bloodbank/password_bloodbank.html", context)
        from_email = settings.EMAIL_HOST_USER
        to_email = [instance.user.email]
        password_email = EmailMessage(subject, message, from_email, to_email)
        password_email.content_subtype = "html"
        password_email.send()
    
    
    
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

# @receiver(post_save, sender=Donation)
# def create_blood_object(sender, instance, created, **kwargs):
#     if created:
#         blood_type = instance.donor.blood_group.blood_group
#         bloodbank = instance.bloodbank
#         blood = Blood.objects.filter(bloodbank=bloodbank, type=blood_type).first()
#         if not blood:
#             blood = Blood.objects.create(bloodbank=bloodbank, type=blood_type)
#         blood.save()
