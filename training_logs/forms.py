from django import forms
from .models import Topic, Entry

#Used to create Forms 
class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text':''}

methods = [
    ('TSE','TSE'),
    ('Remote','Remote'),
    ('In Flight','In Flight'),
    ('Class','Class'),
    ('Self Study','Self Study'),
    ('DSE', 'DSE'),
    ('CSPT','CSPT'),
    ('Global','Global'),
    ('CMCT','CMCT'),
    ('DLPT','DLPT'),
    ('OPI','OPI'),
]
class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['method_of_training','hours','date_training_conducted','text']
        labels = {'Method of Training':'method_of_training','text':'Training Summary','hours':'Hours','date_training_conducted':'Date of Training (yyyy-mm-dd)'}
        widgets = {'text':forms.Textarea(attrs={'cols':80}),
                'method_of_training':forms.Select(choices=methods)}
