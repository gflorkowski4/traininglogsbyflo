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
sources = [
    ('Netflix','Netflix'),
    ('YouTube','YouTube'),
    ('News Site','News Site'),
    ('Educational Site','Educational Site'),
    ('N/A','N/A')
]
class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['method_of_training','hours','date_training_conducted','source']
        labels = {'method_of_training':'Method of Training','hours':'Hours','date_training_conducted':'Date of Training (yyyy-mm-dd)','source':'Source'}
        widgets = {'method_of_training':forms.Select(choices=methods),'source':forms.Select(choices=sources), 'date_training_conducted':forms.SelectDateWidget()}
