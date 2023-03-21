from django.db import models
from accounts_app.models import User
from blooddrop.models import BaseModel, Address

class BloodBank(BaseModel, Address):
    user = models.OneToOneField(User, related_name='bloodbank', on_delete=models.CASCADE)
    logo = models.ImageField(blank=True, null=True)
    iso_certified = models.BooleanField(default=False)
    certificate = models.FileField(upload_to=None, max_length=100)

    class Meta:
        verbose_name = "Blood Bank"
        verbose_name_plural = "Blood Banks"

    def __str__(self):
        return str(self.user.name)
    
class CampSchedule(models.Model):
    bloodbank = models.ForeignKey(BloodBank, related_name='schedule', on_delete=models.CASCADE)
    date = models.DateTimeField()
    starttime = models.TimeField()
    endtime = models.TimeField()
    address = models.TextField()
    pincode = models.IntegerField()

    class Meta:
        verbose_name = "Schedule"
        verbose_name_plural = "Schedules"

    def __str__(self):
        return str(self.date)
    

class Donation(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donation')
    donation_date = models.DateTimeField(auto_now_add=True)
    bloodbank = models.ForeignKey(BloodBank, related_name='donation', on_delete=models.CASCADE)

