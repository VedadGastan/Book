from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy
import random
import string
import time

def generate_code():
    timestamp = str(int(time.time()))
    random_chars1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    random_chars2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return f"{random_chars1}_{timestamp}_{random_chars2}"

# Create your models here.
class Email(models.Model):
    email = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "Emails"
    
    def __str__(self):
        return self.email

class CustomAccountManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, username, password, **other_fields):
        if not username:
            raise ValueError(gettext_lazy('You must provide a username'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, username, password, **other_fields):
        other_fields.setdefault('is_staff', False)
        other_fields.setdefault('is_superuser', False)
        other_fields.setdefault('code', generate_code())
        return self._create_user(email, username, password, **other_fields)

    def create_superuser(self, email, username, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('code', 1)
        
        if other_fields.get('is_staff') is not True: 
            raise ValueError('Superuser must be assigned to is_staff=True.') 
        if other_fields.get('is_superuser') is not True: 
            raise ValueError('Superuser must be assigned to is_superuser=True.')
    
        return self._create_user(email, username, password, **other_fields)


class NewUser(AbstractUser):
    email = models.EmailField(gettext_lazy('email address'), unique=True) 
    username = models.CharField(max_length=150, unique=True) 
    
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    code = models.CharField(max_length=150, default=generate_code())
    secondary_code = models.CharField(max_length=150, blank=True, null=True, unique=True)
    balance = models.IntegerField(default=0)
    
    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username