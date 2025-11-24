from email.policy import default
from random import choice
from tabnanny import verbose
from telnetlib import STATUS

from django.db import models
from accounts.models import CustomUser

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории')

    def __str__(self):
        return self.name


class Application(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress','Принято в работу'),
        ('completed', 'Выполнено'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    title = models.CharField(max_length=200, verbose_name='название')
    description = models.TextField(verbose_name='Описание')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    image = models.ImageField(upload_to='applications/', verbose_name='Изображение помещения')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new' ,verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name = 'Дата создания')
    updated_at = models.DateTimeField(auto_now_add = True, verbose_name='Дата обновления')
    comment = models.TextField(blank=True, verbose_name='Комментарий администратора')
    design_image = models.ImageField(upload_to='designs/', blank=True, verbose_name = 'Изображение дизайна')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title