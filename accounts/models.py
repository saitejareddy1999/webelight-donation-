from django.contrib.auth.models import User
from django.db import models


# class Base(models.Model)

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=11)
    otp = models.CharField(max_length=6)

    # def __str__(self):
    #     return str(user)
