from django.contrib import admin
from bloodbank.models import BloodBank,CampSchedule, Donation

admin.site.register(BloodBank)
admin.site.register(CampSchedule)
admin.site.register(Donation)