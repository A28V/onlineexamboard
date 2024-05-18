from django.db import models
from django.utils.text import slugify


class UsersConfig(models.Model):
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    otp = models.CharField(max_length=6, blank=True, null=True)  # New field for OTP
    otp_verification = models.BooleanField(default=False)  # OTP verification status
    otp_expire = models.DateTimeField(blank=True, null=True)  # OTP expiration datetime

    def __str__(self):
        return self.email  # Modify as per your requirement

    class Meta:
        verbose_name_plural = "Users Configuration"
