from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    user_in_migrations = True
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        user = self.create_user(email,password=password,)
        user.is_admin = True
        user.save(using=self.db)
        return user