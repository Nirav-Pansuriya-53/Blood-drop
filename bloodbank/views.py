import os
from django.shortcuts import redirect
from django.urls import reverse_lazy

from django.views import View
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView 
from django.views.generic.edit import UpdateView 
from django.views.generic.edit import DeleteView
from django.views.generic.detail import DetailView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic.edit import FormMixin

from accounts_app.form import SignUpForm
from bloodbank.forms import AddBloodForm, CampUpdateForm
from accounts_app.models import User

from bloodbank.models import Blood, BloodBank 
from bloodbank.models import Donation
from bloodbank.models import CampSchedule

from django.db.models import Q
from django.db.models import Count

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.contrib import messages

from blooddrop import settings

from django.db.models import Q
from bloodbank.forms import DonationForm
from bloodbank.forms import CampScheduleForm
from bloodbank.forms import RequestForm
from datetime import timedelta,datetime, timezone
from django.db.models import Max
from django.forms.widgets import HiddenInput

# Create your views here.


class IndexView(DetailView, LoginRequiredMixin, CreateView):   
    model = BloodBank
    form_class = AddBloodForm
    template_name="bloodbank/index_bloodbank.html"
    login_url = "/bloodbank/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bloodbank = self.object
        
        context['A1'] = bloodbank.bloods.filter(type='A+').count()
        context['A2'] = bloodbank.bloods.filter(type='A-').count()
        context['B1'] = bloodbank.bloods.filter(type='B+').count()
        context['B2'] = bloodbank.bloods.filter(type='B-').count()
        context['AB1'] = bloodbank.bloods.filter(type='AB+').count()
        context['AB2'] = bloodbank.bloods.filter(type='AB-').count()
        context['O1'] = bloodbank.bloods.filter(type='O+').count()
        context['O2'] = bloodbank.bloods.filter(type='O-').count()
        context['total_unit'] = bloodbank.bloods.count()

        return context

    def form_valid(self, form):
        form.instance.user = self.request.user.bloodbank.id
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['bloodbank'].widget = HiddenInput()
        form.fields['bloodbank'].initial = self.request.user.bloodbank
        return form
    
    def get_success_url(self):
        return reverse_lazy('index1', kwargs={'pk': self.request.user.bloodbank.id})
         

class BloodBankHistory(ListView):
    model = Donation
    template_name = "bloodbank/bloodbank_history.html"
    context_object_name = 'bloodbank'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(bloodbank_id=self.kwargs['pk'])
        return queryset
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     donations = self.object.donation.all()
    #     donation_data = []
        
    #     for donation in donations:
    #         donor = donation.donor
    #         bloodbank = donation.bloodbank
    #         blood_group = donor.blood_group.blood_group if hasattr(donor, 'blood_group') else None
    #         donation_data.append({
    #             'donation_date': donation.donation_date,
    #             'donor_name': donor.name,
    #             'bloodbank_name': bloodbank.user.name,
    #             'blood_group': blood_group
    #         })
    #     context['donation_data'] = donation_data
    #     return context
    


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'bloodbank/signin_bloodbank.html'
    
    def form_valid(self, form):
        email = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return super().form_valid(form)
        form.add_error(None, 'Invalid email address or password')
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse_lazy('index1', kwargs={'pk': self.request.user.bloodbank.id})


class SignupView(CreateView):
    form_class = RequestForm
    template_name = "bloodbank/signup_bloodbank.html"
    success_url = "/user/index/"


class DonorView(ListView):
    model = User
    template_name = "bloodbank/donor_bloodbank.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = User.objects.filter(Q(email__icontains=query)).annotate(
            latest_donation_date=Max('donation__donation_date')
        ).order_by('-latest_donation_date')
        return object_list

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if not self.get_queryset():
            messages.warning(request, 'User does not exist.')
            return redirect('index1', pk=self.request.user.bloodbank.pk)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["timedelta"] = timedelta(days=90)
        context["today"] = datetime.today()
        return context



class DonationCreateView(LoginRequiredMixin, CreateView):
    model = Donation
    template_name = 'bloodbank/donation_form_bloodbank.html'
    form_class = DonationForm
    login_url = '/bloodbank/login/'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['bloodbank'].widget = HiddenInput()
        form.fields['bloodbank'].initial = self.request.user.bloodbank
        return form
    
    def get_success_url(self):
        return reverse_lazy('index1', kwargs={'pk': self.request.user.bloodbank.id})


class CampScheduleView(CreateView):
    model = CampSchedule
    template_name = 'bloodbank/camp_schedule_bloodbank.html'
    form_class = CampScheduleForm
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['bloodbank'].widget = HiddenInput()
        form.fields['bloodbank'].initial = self.request.user.bloodbank
        return form

    def get_success_url(self):
        return reverse_lazy('index1', kwargs={'pk': self.request.user.bloodbank.id})
    
class CampScheduleUpdateView(UpdateView):
    model = CampSchedule
    form_class = CampUpdateForm
    template_name = 'bloodbank/camp_update.html'
    success_url = "/bloodbank/camp-schedule/"

    # def get_queryset(self):
    #     # Get the current date and time
    #     now = datetime.now()
    #     # Filter the queryset to exclude past camps
    #     queryset = CampSchedule.objects.filter(
    #         pk=self.kwargs['pk'],
    #         date__gte=now,
    #     )
    #     return queryset
    

class CampScheduleDeleteView(DeleteView):
    model = CampSchedule
    template_name = 'bloodbank/camp_delete.html'

class CampScheduleDisplayView(ListView):
    model = CampSchedule
    template_name = 'bloodbank/camp_display.html'
    context_object_name = 'camp_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["today"] = datetime.today()
        return context

    def get_queryset(self):
        return CampSchedule.objects.filter(bloodbank=self.request.user.bloodbank)


class UserSignupFromBloodbankView(CreateView):   
    model = User
    template_name="bloodbank/user_signup_bloodbank.html" 
    form_class = SignUpForm

    def get_success_url(self):
        return reverse_lazy('index1', kwargs={'pk': self.request.user.bloodbank.id})

class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect("index")
    

class BloodBankProfileView(DetailView):
    template_name = "bloodbank/display_bloodbank_profile.html"
    model = BloodBank
    context_object_name = 'bloodbank'


class LogoView(TemplateView):
    template_name = 'logo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo_url'] = settings.MEDIA_URL + 'path/to/logo.jpg'
        return context


class BloodBankProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'bloodbank/update_profile_bloodbank.html'
    fields = ['name', 'phone_number', 'address', 'city', 'state']

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('bloodbank_profile', kwargs={'pk': self.request.user.bloodbank.id})

   
class BloodBankLogoUpdateView(LoginRequiredMixin, UpdateView):
    model = BloodBank
    template_name = 'bloodbank/update_profile_logo.html'
    fields = ['logo']

    def get_success_url(self):
        return reverse_lazy('bloodbank_profile', kwargs={'pk': self.request.user.bloodbank.id})
    