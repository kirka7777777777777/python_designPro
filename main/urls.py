from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
path('profile/', views.profile, name='profile'),
    path('create/', views.create_application, name='create_application'),
    path('delete/<int:pk>/', views.delete_application, name='delete_application'),
]