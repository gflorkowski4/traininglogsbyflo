from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here 
class Profile(models.Model):
    """Custom Profile for app"""
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, default='Green Team')

    def __str__(self):
        return str(self.user)




class Topic(models.Model):
    """A topic that the user is learning about."""
    text = models.CharField(max_length=200)
    data_added = models.DateTimeField(auto_now_add = True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        """Return a string representation of the model"""
        return f' {self.text} created by: {self.owner}'

class Entry(models.Model):
    """Something Learned about the topic."""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    method_of_training = models.CharField(max_length=200)
    source = models.CharField(max_length=20)
    hours = models.FloatField()
    date_training_conducted = models.DateField()
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'
    
    def __str__(self):
        """Return a string representation"""
        return f'{self.topic.text} | {self.topic.owner.first_name} {self.topic.owner.last_name} | {self.method_of_training} | {self.hours} hours'

    def month_published(self):
        """Used to sort the entries by month for record purposes"""
        return self.date_training_conducted.strftime('%B')

    
        
