from django.views.generic.list import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, FormView
from django.views.generic import FormView
from bloodbank.models import BloodBank, Donation, CampSchedule
from accounts_app.models import User,BloodGroup
from django.db.models import Q
from django.views.generic.detail import DetailView
from django.db.models import Count
from blooddrop import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.views.generic.edit import FormMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from bloodbank.forms import DonationForm
from datetime import timedelta,datetime

# Create your views here.

class IndexView(TemplateView):   
    model = BloodBank
    template_name="bloodbank/index_bloodbank.html"
     

class BloodBankHistory(DetailView):
    model = BloodBank
    template_name = "bloodbank/bloodbank_history.html"
    context_object_name = 'bloodbank'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        donations = self.object.donation.all()
        donation_data = []
        
        for donation in donations:
            donor = donation.donor
            bloodbank = donation.bloodbank
            blood_group = donor.blood_group.blood_group if hasattr(donor, 'blood_group') else None
            donation_data.append({
                'donation_date': donation.donation_date,
                'donor_name': donor.name,
                'bloodbank_name': bloodbank.user.name,
                'blood_group': blood_group
            })
        context['donation_data'] = donation_data
        return context

class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'bloodbank/signin_bloodbank.html'
    success_url = '/bloodbank/index/'
    
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
    


User = get_user_model()

class DonorView(LoginRequiredMixin, ListView):
    model = User
    template_name = "bloodbank/donor_bloodbank.html"
    login_url = '/bloodbank/login/'

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = User.objects.filter(Q(email__icontains=query)) 
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["timedelta"] = timedelta(days=90)
        context["today"] = datetime.today()
        return context



class DonationCreateView(LoginRequiredMixin, CreateView):
    model = Donation
    template_name = 'bloodbank/donation_form_bloodbank.html'
    form_class = DonationForm
    success_url = '/bloodbank/index/'
    login_url = '/bloodbank/login/'
