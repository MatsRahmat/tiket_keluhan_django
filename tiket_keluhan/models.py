from django.db import models
from django.contrib.auth.models import AbstractUser
from tiket_keluhan.enums import RoleEnum
from datetime import date

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

class TiketModel(models.Model):
    executor_id = models.ForeignKey(CustomUserModel, null=True, on_delete=models.CASCADE, related_name='tiket_executor')
    no_tiket = models.CharField('No Tiket', null=False, blank=False, max_length=50)
    login_id = models.CharField('Login Id', null=False, blank=False)
    subject = models.CharField('Subject', null=False, blank=False, max_length=255)
    description = models.TextField('Description', null=False, blank=False)
    updated_at = models.DateTimeField('updated_at', auto_now=True)
    created_at = models.DateTimeField('created_at', auto_now_add=True)
    
    def save(self,*args,**kwargs):
        if not self.no_tiket:
            today = date.today().strftime("%y%m%d")
            last_tiket = TiketModel.objects.filter(no_tiket__startswith=today).order_by("no_tiket").last()
            if last_tiket:
                last_no = int(last_tiket.no_tiket.split("-")[1])
                new_no = last_no + 1
            else:
                new_no = 1
            padded_no = str(new_no).zfill(5)
            self.no_tiket = f"{today}-{padded_no}"

        super().save(*args,**kwargs)
        
    def __str__(self):
        return self.no_tiket