from django.views.generic import CreateView,ListView
from django.views import View
from django.views.generic.base import TemplateView
from .form import SignUpForm,LoginForm,OTPForm
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic.edit import CreateView,FormView
from django.conf import settings
from datetime import datetime
from django.contrib import messages
import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.contrib.auth.views import auth_login
from django.shortcuts import HttpResponseRedirect,redirect
from django.http import HttpResponse
from django.views import View
from django.conf import settings
from io import BytesIO
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw, ImageFont
from django.views.generic import DetailView
from accounts_app.models import User
from bloodbank.models import Donation,CampSchedule
from django.contrib.auth.views import LogoutView
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from datetime import date

# index view for user 
class IndexView(TemplateView):   
    template_name="user/index1.html"


class AboutView(TemplateView):
    template_name="user/about1.html"


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'user/signup.html'
    success_url = '/user/verify-otp/'
    # def dispatch(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> http.HttpResponse:
    #     return super().dispatch(request, *args, **kwargs)
    def form_valid(self, form):
        super().form_valid(form)
        email = form.cleaned_data.get('email')
        user = form.instance
        otp = random.randrange(111111, 999999)

        subject = 'Your OTP for logging in to our site'
        context = {"otp": otp, "user": user, "year": (date.today()).year}
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

        return HttpResponseRedirect(reverse("verify-otp", kwargs={"user_id": user.id}))


# For the demo
class VerifyOtpView(FormView):
    form_class = OTPForm
    success_url = '/user/index/'
    template_name = 'user/verify_otp.html'

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs["user_id"] = self.kwargs.get("user_id")
        return form_kwargs

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())
    
    def get_context_data(self, **kwargs,):
        context =  super().get_context_data(**kwargs)
        context["user_id"] = self.kwargs.get("user_id")
        return context


class LoginView(FormView):
    template_name = "user/login.html"
    form_class = LoginForm
    success_url = '/verify-otp/'

    def form_valid(self, form):
        user = form.get_user()
        messages.success(self.request, 'An OTP has been sent to your email.')
        return HttpResponseRedirect(reverse("verify-otp", kwargs={"user_id": user.id}))



class CertificateView(View):
    def get(self, request, donation_pk):
        # Get the donor details from the database or request
        donation = Donation.objects.get(pk=donation_pk)
        donor_name = donation.donor.name
        donation_date = donation.donation_date.strftime('%B %d, %Y')
        blood_type = donation.donor.blood_group.blood_group

        # Create a ByteIO buffer to receive PDF data.
        buffer = BytesIO()

        # Create the PDF object, using the BytesIO object as its "file."
        p = canvas.Canvas(buffer)

        # Add the background image to the PDF.
        bg_image_path = "accounts_app\static\images\cirti2.jpeg"
        p.drawImage(bg_image_path, 0, 0, width=p._pagesize[0], height=p._pagesize[1])
        p.setFillColorRGB(1, 0, 0)


        # Add the certificate details to the PDF.
        p.drawString(250, 380, "Mr./Ms. " + donor_name)
        p.drawString(200, 340, "has donated blood on " + donation_date)
        p.setFillColorRGB(1, 0, 0)
        p.drawString(230, 310, "and has a blood type of " + blood_type)
        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        buffer.seek(0)
        filename = 'certificate.pdf'
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response

class DonationHistory(LoginRequiredMixin, DetailView):
    login_url = 'login'
    model = User
    template_name = 'user/doner_history.html' 
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['donations'] = self.object.donation.all()
        return context
    
class LogoutView(View):

    def get(self, request):
        logout(request)
        messages.info(request, "You have successfully logged out.")
        return redirect("index")

class CampList(ListView):
    model = CampSchedule
    context_object_name = 'camp_obj'
    template_name='user/index1.html'
   



# def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(
#             data=request.data, context={"request": request}
#         )
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()

#         user.otp_key = random_hex(20)
#         user.save()

#         totp = TOTPVerification(user.otp_key).generate_token()
#         user_otp = UserOTP()

#         subject = "Confirm your email"
#         template = "registration/reset-password.html"
#         user_otp.send_otp_in_email(request, user, totp, template, subject)

#         user_otp.send_otp_in_sms(user, "Registartion", totp)

#         welcome_subject = "Welcome to BloodDrop"
#         context = {"user": user,"year": (date.today()).year}
#         welcome_message = render_to_string("registration/bustto_welcome.html", context)
#         welcome_email = EmailMessage(
#             welcome_subject,
#             welcome_message,
#             settings.EMAIL_HOST_USER,
#             [user.email],
#         )
#         welcome_email.content_subtype = "html"
#         welcome_email.send()

#         return Response(
#             {"detail": "User has been registered."}, status=status.HTTP_200_OK
#         )