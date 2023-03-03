from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from otp.models import Device
from phonenumber_field.phonenumber import PhoneNumber
from .models import User

class CustomBackend(ModelBackend):
    def authenticate(self, request, phone_number=None, otp=None, **kwargs):
        try:
            phone_number = PhoneNumber.from_string(phone_number)
            user = User.objects.get(phone_number=phone_number)
            if user.is_verified:
                if otp:
                    device = Device.from_persistent_id(user.phone_number.as_e164)
                    if device.verify_token(otp):
                        return user
                    else:
                        raise ValidationError(_('Invalid OTP'))
            else:
                raise ValidationError(_('Mobile number is not verified'))
        except User.DoesNotExist:
            raise ValidationError(_('Invalid mobile number'))
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
