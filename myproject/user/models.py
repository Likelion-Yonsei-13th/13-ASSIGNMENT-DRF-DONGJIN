from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

#AbstractUser 상속
class CustomUser(AbstractUser):
    #username, email, password 등은 이미 포함
    nickname = models.CharField(max_length=30, blank = True)
    provider = models.CharField(max_length=20, blank = True)

    def __str__(self):
        return self.nickname