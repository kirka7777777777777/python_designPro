from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
import re


class CustomUserCreationForm(UserCreationForm):
    fio = forms.CharField(max_length=255, label='ФИО')
    email = forms.EmailField(required=True)
    agree = forms.BooleanField(required=True, label='Согласие на обработку персональных данных')

    class Meta:
        model = CustomUser
        fields = ('fio', 'username', 'email', 'password1', 'password2', 'agree')

    def clean_fio(self):
        fio = self.cleaned_data.get('fio')
        if not re.match(r'^[а-яА-ЯёЁ\s\-]+$', fio):
            raise forms.ValidationError('ФИО должно содержать только кириллические буквы, дефисы и пробелы')
        return fio

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z\-]+$', username):
            raise forms.ValidationError('Логин должен содержать только латинские буквы и дефисы')
        return username