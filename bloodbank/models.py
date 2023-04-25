from django.db import models
from accounts_app.models import User
from blooddrop.models import BaseModel, Address
from datetime import datetime
from  phonenumber_field.modelfields import PhoneNumberField
from django.db.models import Count



class BloodBank(BaseModel, Address):
    user = models.OneToOneField(User, related_name='bloodbank', on_delete=models.CASCADE)
    iso_certified = models.BooleanField(default=False)
    certificate = models.FileField(upload_to='cirtificate', max_length=100)
    logo = models.ImageField(upload_to='bloodbank_logo/', null=True, blank=True)

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
    donation_date = models.DateTimeField(default=datetime.now)
    bloodbank = models.ForeignKey(BloodBank, related_name='donation', on_delete=models.CASCADE)

    class Meta:
        get_latest_by = '-donation_date'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        blood_type = self.donor.blood_group.blood_group
        Blood.objects.create(bloodbank=self.bloodbank, donation=self, type=blood_type)


class Blood(models.Model):
    A_POSITIVE = 'A+'
    A_NEGATIVE = 'A-'
    B_POSITIVE = 'B+'
    B_NEGATIVE = 'B-'
    O_POSITIVE = 'O+'
    O_NEGATIVE = 'O-'
    AB_POSITIVE = 'AB+'
    AB_NEGATIVE = 'AB-'
    
    BLOOD_GROUP_CHOICES = [
        (A_POSITIVE, 'A+'),
        (A_NEGATIVE, 'A-'),
        (B_POSITIVE, 'B+'),
        (B_NEGATIVE, 'B-'),
        (O_POSITIVE, 'O+'),
        (O_NEGATIVE, 'O-'),
        (AB_POSITIVE, 'AB+'),
        (AB_NEGATIVE, 'AB-'),
    ]
    
    bloodbank = models.ForeignKey(BloodBank, related_name='bloods', on_delete=models.CASCADE)
    donation = models.ForeignKey(Donation, related_name='bloods', on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)

class Request(BaseModel, Address):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = PhoneNumberField(db_index=True)

