from django import forms
from .models import Topic, Entry

#Used to create Forms 
class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text':''}

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['hours','date_training_conducted','text']
        labels = {'text':'','hours':'Hours','date_training_conducted':'Date of Training (yyyy-mm-dd)'}
        widgets = {'text':forms.Textarea(attrs={'cols':80})}
