from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValidationError("The Email field must be set.")
        if not first_name:
            raise ValidationError("The First Name field must be set.")
        if not last_name:
            raise ValidationError("The Last Name field must be set")
        
        email = self.normalize_email(email)
        
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_active=True)
        user.set_password(raw_password=password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password=None,):
        user = self.create_user(email, first_name, last_name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
    