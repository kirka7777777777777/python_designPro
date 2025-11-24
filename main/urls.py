from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
path('profile/', views.profile, name='profile'),
    path('create/', views.create_application, name='create_application'),
    path('delete/<int:pk>/', views.delete_application, name='delete_application'),
path('superadmin/', views.admin_panel, name='admin_panel'),
path('superadmin/change-status/<int:pk>/', views.change_application_status, name='change_status'),
path('superadmin/delete-category/<int:pk>/', views.delete_category, name='delete_category'),
]