from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here 
class Topic(models.Model):
    """A topic that the user is learning about."""
    text = models.CharField(max_length=200)
    data_added = models.DateTimeField(auto_now_add = True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        """Return a string representation of the model"""
        return self.text

class Entry(models.Model):
    """Something Learned about the topic."""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    hours = models.IntegerField()
    date_training_conducted = models.DateField()
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'
    
    def __str__(self):
        """Return a string representation"""
        return f'{self.text[:50]}...'

    def month_published(self):
        """Used to sort the entries by month for record purposes"""
        return self.date_training_conducted.strftime('%B')

    
        
