from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUserModel(AbstractUser):
    login_id = models.CharField("Login id", blank=False, null=False,max_length=200)
    
    def __str__(self):
        return f"{self.login_id} - {self.username}"
    