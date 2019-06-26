from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
    
class Profile(models.Model):
    p_user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    p_name = models.CharField(max_length=5, verbose_name="이름")
    p_grade = models.CharField(max_length=1, verbose_name="학년")
    p_birth_date = models.DateField(verbose_name="생년월일", null=True)


