from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from training_logs.models import Profile
from django import forms 

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('username','first_name','last_name','password1','password2')
class EditUserForm(UserChangeForm):
    class Meta:
        model = User
        fields =  ('username','first_name','last_name',)

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['role']