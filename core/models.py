from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    phone_number = models.CharField(max_length=11, unique=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username
