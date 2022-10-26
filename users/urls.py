"""Defines URL Patterns for views"""
from django.urls import path, include
from django.contrib.auth import views as auth_views
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
    path('search_results/', views.search_results, name='search_results'),
    path('password/',auth_views.PasswordChangeView.as_view(template_name='registration/change_password.html'),name='change_password'),
    path('password_change_done', views.password_change, name='password_change'),
]
