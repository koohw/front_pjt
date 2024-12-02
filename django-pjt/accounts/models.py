# accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    profile_picture = models.ImageField(upload_to="images/", null=True, blank=True, default="images/base.png")
    bio = models.TextField(blank=True, null=True)  # 사용자 소개
    address = models.CharField(max_length=255, blank=True, null=True)  # 주소
    join_date = models.DateField(auto_now_add=True)
    token = models.IntegerField(default=100)

    def __str__(self):
        return self.username
