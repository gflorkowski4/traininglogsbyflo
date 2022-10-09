from django.shortcuts import render, redirect 
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from training_logs.models import Entry

# Create your views here for Users app
def register(request):
    """Register a new user."""
    if request.method != 'POST':
        #Display Blank Registration Form
        form = UserCreationForm()
    else:
        # Process completed form
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # Log-in the user and redirect to home page
            login(request, new_user)
            return redirect('training_logs:index')
    # display a blank or invalid form 
    context = {'form':form}
    return render(request, 'registration/register.html', context)

def dashboard(request):
    """Dashboard to present data"""
    entries = Entry.objects.all()
    return render(request, 'registration/dashboard.html', {'entries':entries} )
    