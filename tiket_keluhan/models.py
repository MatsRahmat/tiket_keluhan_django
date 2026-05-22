import os
from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractUser
from tiket_keluhan.enums import RoleEnum, TiketStatusEnum

from tiket_keluhan.utils import (
    custom_upload_path
)

# Create your models here.
# ==================================
#            USER MODEL
# ==================================
class CustomUserModel(AbstractUser):
    login_id = models.CharField("Login id",blank=False, null=False, max_length=200,unique=True)
    role     = models.IntegerField("role", blank=False, null=False, default=RoleEnum.staff.value)
    user_id  = models.CharField("User Id", blank=True, null=True, max_length=4, unique=True)
    
    USERNAME_FIELD = 'login_id'
    REQUIRED_FIELDS=['username']
    
    def save(self, *args, **kwargs):
        # Membuat agar login id tetap lower case
        self.login_id = self.login_id.lower()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.login_id} - {self.username}"

# ==================================
#            TIKET MODEL
# ==================================
class TiketModel(models.Model):
    no_tiket = models.CharField('No Tiket', null=False, blank=False, max_length=50)
    login_id = models.CharField('Login Id', null=False, blank=False)
    subject = models.CharField('Subject', null=False, blank=False, max_length=255)
    description = models.TextField('Description', null=False, blank=False)
    status = models.CharField('Status', max_length=50, null=False, blank=False, default=TiketStatusEnum.SENT.value)
    operator = models.ForeignKey(CustomUserModel, null=True, on_delete=models.SET_NULL, related_name='tiket_operator')
    executor = models.ForeignKey(CustomUserModel, null=True, on_delete=models.CASCADE, related_name='tiket_executor')
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

        # if not self.status:
        #     # Set status ketika pertama kali dibuat
        #     self.status = TiketStatus.SENT.value
        
        super().save(*args,**kwargs)
        
    def __str__(self):
        return self.no_tiket

# ==================================
#       TIKET ATTACHMENT MODEL
# ==================================    
class TiketAttachmentModel(models.Model):
    tiket = models.OneToOneField(TiketModel, on_delete=models.CASCADE, related_name='attachment')
    file = models.FileField(upload_to=custom_upload_path)
    original_name = models.CharField('original name', max_length=255)
    sotred_name = models.CharField('stored name', max_length=255)
    created_at = models.DateTimeField('created_at', auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if self.id:
            old_file = TiketAttachmentModel.objects.get(id=self.id).file
            if old_file and old_file != self.file and os.path.isfile(old_file.path):
                os.remove(old_file.path)
        
        if self.file and not self.original_name:
            self.original_name = os.path.basename(self.file.name)
            
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.original_name


# ==================================
#            TIKET ACTION
# ==================================  
class TiketActionModel(models.Model):
    tiket = models.ForeignKey(TiketModel, on_delete=models.CASCADE, related_name="actions")
    aktor = models.ForeignKey(CustomUserModel, on_delete=models.SET_NULL, null=True, related_name='actions_actor')
    action_type = models.CharField('action type',max_length=50)
    note = models.TextField('note',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.tiket.no_tiket} - {self.action_type}"
    

# ==================================
#         TIKET REVIEWER
# ==================================      
class ReviewerModel(models.Model):
    tiket = models.ForeignKey(TiketModel, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(CustomUserModel, on_delete=models.SET_NULL, null=True, related_name="given_reviews")
    evaluation = models.TextField()
    rating = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
     
    def __str__(self):
        return f"{self.tiket.no_tiket} - {self.reviewer.username}"
    
    
# ==================================
#           TIKET HISTORY
# ==================================  
class TiketStatusHistory(models.Model):
    tiket = models.ForeignKey(TiketModel, on_delete=models.CASCADE, related_name="status_history")
    changed_by = models.ForeignKey(CustomUserModel, on_delete=models.SET_NULL, null=True, related_name="status_change")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.tiket.no_tiket} - {self.timestamp}"