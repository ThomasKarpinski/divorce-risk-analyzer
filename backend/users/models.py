from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    birthdate = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], null=True, blank=True)
    education = models.CharField(max_length=20, choices=[('primary', 'Primary'), ('secondary', 'Secondary'), ('bachelor', 'Bachelor'), ('master', 'Master'), ('phd', 'PhD')], null=True, blank=True)
    residence = models.CharField(max_length=20, choices=[('small', 'Small City / Town'), ('large', 'Large City')], null=True, blank=True)