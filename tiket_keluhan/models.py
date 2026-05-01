from django.db import models
from django.contrib.auth.models import AbstractUser
from tiket_keluhan.enums import RoleEnum

# Create your models here.
class CustomUserModel(AbstractUser):
    login_id = models.CharField("Login id",blank=False, null=False,max_length=200,unique=True)
    role = models.IntegerField("role", blank=False, null=False, default=RoleEnum.staff.value)
    
    USERNAME_FIELD = 'login_id'
    REQUIRED_FIELDS=['username']
    
    def save(self, *args, **kwargs):
        # Membuat agar login id tetap lower case
        self.login_id = self.login_id.lower()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.login_id} - {self.username}"
