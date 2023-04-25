from django.db import models
from django.contrib.auth.models import  AbstractBaseUser
from .manager import UserManager
from  phonenumber_field.modelfields import PhoneNumberField
from blooddrop.models import Address

class User(AbstractBaseUser, Address):
  
    username = None
    name = models.CharField(max_length=20)
    email = models.EmailField(verbose_name='email address',max_length=255,unique=True,db_index=True)
    phone_number = PhoneNumberField(db_index=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    otp_create_at = models.DateTimeField(null=True, blank=True)
    otp = models.IntegerField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    weight= models.IntegerField(null=True, blank=True)
    is_bloodbank = models.BooleanField(default=False, null=True, blank=True)
    logo = models.ImageField(upload_to='bloodbank_logo/', null=True, blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    
    @property
    def group(self):
        blood_group = getattr(self, "blood_group", None)
        if blood_group:
            return blood_group.blood_group
    
class BloodGroup(models.Model):
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
    
    user = models.OneToOneField(User, related_name='blood_group', on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)

REQUEST_STATUS_CHOICES = [    ('Pending', 'Pending'),    ('Accepted', 'Accepted'),    ('Rejected', 'Rejected')]
class BloodRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bloodbank = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blood_requests')
    blood_group = models.CharField(max_length=3, choices=BloodGroup.BLOOD_GROUP_CHOICES)
    quantity = models.IntegerField()
    status = models.CharField(choices=REQUEST_STATUS_CHOICES, max_length=10, default='Pending')
    requested_at = models.DateTimeField(auto_now_add=True)