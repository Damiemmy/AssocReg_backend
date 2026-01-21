from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(unique=True, max_length=100,blank=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    reg_number= models.CharField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    otp = models.CharField(max_length=100, null=True, blank=True)
    refresh_token = models.CharField(max_length=1000, null=True, blank=True)

    USERNAME_FIELD = 'reg_number'
    REQUIRED_FIELDS = ['username','email']
    def __str__(self):
        return self.reg_number
    
    def save(self, *args, **kwargs):
        if not self.username and self.email:
            self.username = self.email.split('@')[0]
        super(User, self).save(*args, **kwargs)

