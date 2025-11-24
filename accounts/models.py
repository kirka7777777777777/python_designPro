from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    fio = models.CharField(max_length=255, verbose_name='ФИО')

    def __str__(self):
        return self.username
