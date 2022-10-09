"""Defines URL Patterns for Training Logs"""
from django.urls import path
from . import views


app_name = 'training_logs'
urlpatterns = [
    # Home Page
    path('',views.index, name='index'),
    # Topics page
    path('topics/', views.topics, name='topics'),
    # Detail Page for a single Topic
    path('topics/<int:topic_id>', views.topic, name='topic'),
    # Page for adding new Training Topic
    path('new_topic/', views.new_topic, name='new_topic'),
    # Page For adding a New Entry
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    # Page for editing an entry 
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    
    
]
