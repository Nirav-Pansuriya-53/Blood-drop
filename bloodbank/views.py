from django.shortcuts import render
from django.views.generic.list import ListView
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, FormView
from django.views.generic import FormView
from bloodbank.models import BloodBank, Donation
from bloodbank.models import User
from django.db.models import Q

# Create your views here.

class IndexView(TemplateView):   
    template_name="bloodbank/index_bloodbank.html"

class DonorView(ListView):
    model = User
    template_name = "bloodbank/donor_bloodbank.html"
    
    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = User.objects.filter(Q(email__icontains=query))
        return object_list
    

class DonationView(CreateView):
    model = Donation
    fields = ['donor','bloodbank']
    template_name = "bloodbank/donor_bloodbank.html"
    success_url = '/bloodbank/index'

class Donation(ListView):
    model = Donation
    context_object_name = 'donation'
    template_name='bloodbank/donor_bloodbank.html'