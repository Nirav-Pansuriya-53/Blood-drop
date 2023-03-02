from django.db import models
from django.contrib.auth.models import  AbstractBaseUser
from .manager import UserManager
from  phonenumber_field.modelfields import PhoneNumberField

class User(AbstractBaseUser):
    username = None
    email = models.EmailField(verbose_name='email address',max_length=255,unique=True,)
    phone_number = PhoneNumberField()
    address = models.TextField()
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    pincode = models.IntegerField(null=True, blank=True)
    latitude = models.IntegerField(null=True, blank=True)
    longitude = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    otp_create_at = models.DateTimeField(null=True, blank=True)
    otp = models.IntegerField(null=True, blank=True)

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