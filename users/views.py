from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from training_logs.models import Entry, Topic
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .forms import SignUpForm

from datetime import datetime

# Create your views here for Users app


def register(request):
    """Register a new user."""
    if request.method != 'POST':
        # Display Blank Registration Form
        form = SignUpForm()
    else:
        # Process completed form
        form = SignUpForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # Log-in the user and redirect to home page
            login(request, new_user)
            return redirect('training_logs:index')
    # display a blank or invalid form
    context = {'form': form}
    return render(request, 'registration/register.html', context)


@login_required
def dashboard(request):
    """Dashboard to present data"""
    current_month = datetime.now().strftime('%B')
    owner = request.user
    entries = Entry.objects.all()
    topics = Topic.objects.all()
    users = User.objects.all()
    total_hours = {}

    for user in users:
        hours_total = 0
        for entry in entries:
            if entry.month_published() == current_month:
                if user == entry.topic.owner:
                    hours_total += entry.hours
        total_hours[user] = hours_total

    return render(request, 'registration/dashboard.html',
                  {'entries': entries,
                   'topics': topics,
                   'users': users,
                   'owner': owner,
                   'total_hours': total_hours,
                   'current_month': current_month})


@login_required
def admin_dashboard(request):
    if request.user.is_superuser:
        current_month = datetime.now().strftime('%B')
        owner = request.user
        entries = Entry.objects.all()
        topics = Topic.objects.all()
        users = User.objects.all()
        total_hours = {}
        training_method_hours = {}

        for user in users:
            hours_total = 0
            for entry in entries:
                if entry.month_published() == current_month:
                    if user == entry.topic.owner:
                        hours_total += entry.hours
            total_hours[user] = hours_total


        for method in ['TSE', 'Remote','Class','In Flight']:
            method_hours = 0
            for entry in entries:
                if entry.month_published() == current_month:
                    if entry.method_of_training == method:
                        method_hours += entry.hours
            training_method_hours[method] = method_hours
                

        return render(request, 'registration/admin_dashboard.html',
                      {'entries': entries,
                       'topics': topics,
                       'users': users,
                       'owner': owner,
                       'total_hours': total_hours,
                       'training_method_hours': training_method_hours,
                       'current_month': current_month})
    else:
        raise Http404
