"""Defines URL Patterns for views"""
from django.urls import path, include
from . import views


app_name = 'users'
urlpatterns = [
    # include default auth urls
    path('', include('django.contrib.auth.urls')),
    # Path for a registration form
    path('register/', views.register, name='register'),

]
