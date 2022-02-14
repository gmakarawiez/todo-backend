from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager



class CustomUser(AbstractUser):

    username = models.CharField(blank=True, default='', max_length=255, unique = False)
    email = models.EmailField(_('email address'), unique=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
