from django import forms
from bloodbank.models import Blood, Donation,CampSchedule, User, Request
from django.forms import widgets
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['bloodbank','donor']

class CampScheduleForm(forms.ModelForm):
    
    class Meta:
        model = CampSchedule
        fields = ['bloodbank','date','starttime','endtime','address','pincode']
        widgets = {
            'date': widgets.DateInput(attrs={'type': 'date','format': '%Y-%m-%d'}),
            'starttime': widgets.TimeInput(attrs={'type': 'time', 'step': '900'}),
            'endtime': widgets.TimeInput(attrs={'type': 'time', 'step': '900'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        starttime = cleaned_data.get("starttime")
        endtime = cleaned_data.get("endtime")
        date = cleaned_data.get('date')

        if starttime and endtime:
            if starttime >= endtime:
                raise ValidationError("End time must be greater than start time.")
            
        
        if date and date < timezone.now():
            raise forms.ValidationError("Date cannot be in the past.")

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['name','email','phone_number', 'address', 'city', 'state', 'pincode']

class AddBloodForm(forms.ModelForm):
    class Meta:
        model = Blood 
        fields = ['type', 'bloodbank']

class CampUpdateForm(forms.ModelForm):
    class Meta:
        model = CampSchedule
        fields = ['bloodbank', 'date', 'starttime', 'endtime', 'address', 'pincode']

        widgets = {
                'date': widgets.DateInput(attrs={'type': 'date','format': '%Y-%m-%d'}),
                'starttime': widgets.TimeInput(attrs={'type': 'time', 'step': '900'}),
                'endtime': widgets.TimeInput(attrs={'type': 'time', 'step': '900'}),
            }

    def clean(self):
        cleaned_data = super().clean()
        starttime = cleaned_data.get("starttime")
        endtime = cleaned_data.get("endtime")
        date = cleaned_data.get('date')

        if starttime and endtime:
            if starttime >= endtime:
                raise ValidationError("End time must be greater than start time.")
            
        
        if date and date < timezone.now():
            raise forms.ValidationError("Date cannot be in the past.")