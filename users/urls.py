"""Defines URL Patterns for views"""
from django.urls import path, include
from . import views


app_name = 'users'
urlpatterns = [
    # include default auth urls
    path('', include('django.contrib.auth.urls')),
    # Path for a registration form
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('edit_profile/',views.edit_profile, name='edit_profile'), 
    path('search_results/', views.search_results, name='search_results') 
]
