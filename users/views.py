from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.db.models.functions import Extract
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from training_logs.models import Entry, Topic
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .forms import EditProfileForm, SignUpForm

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
    entries = Entry.objects.all().order_by('-date_training_conducted')
    topics = Topic.objects.all()
    users = User.objects.all()
    user_count = User.objects.count()
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
        entries = Entry.objects.all().order_by('-date_training_conducted')
        topics = Topic.objects.all()
        users = User.objects.all()
        total_hours = {}
        training_method_hours = {}
        entry_quarters = {}

        for user in users:
            hours_total = 0
            for entry in entries:
                if entry.month_published() == current_month:
                    if user == entry.topic.owner:
                        hours_total += entry.hours
            total_hours[user] = hours_total

        for method in ['TSE', 'Remote', 'Class', 'In Flight', 'Self Study']:
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
                       'current_month': current_month,
                       })
    else:
        raise Http404


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid:
            form.save()
            return redirect('users:dashboard')
    else:
        form = EditProfileForm(instance=request.user)
        args = {
            'form': form}
        return render(request, 'registration/edit_profile.html', args)


@login_required
def search_results(request):
    training_method_hours = {}
    total_hours = {}
    users = User.objects.all()
    bad_users = {}

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        req_hours = int(request.POST.get('req_hours'))

        # Now the data is the entries that are in between the selected dates.
        data = Entry.objects.filter(
            date_training_conducted__range=(start_date, end_date)).order_by('-date_training_conducted')

        # Query for Each Training Method Totals
        for method in ['TSE', 'Remote', 'Class', 'In Flight', 'Self Study']:
            method_hours = 0
            for entry in data:
                if entry.method_of_training == method:
                    method_hours += entry.hours
            training_method_hours[method] = method_hours

        # User Totals for the queried dates
        for user in users:
            hours_total = 0
            for entry in data:
                if user == entry.topic.owner:
                    hours_total += entry.hours
            total_hours[user] = hours_total

        #people that have not done the correct hours
        for user, hours in total_hours.items():
            if hours < req_hours:
                bad_users[user] = hours

        return render(request, 'registration/search_results.html', {'data': data, 
                                                                    'training_method_hours': training_method_hours,
                                                                    'total_hours':total_hours,
                                                                    'req_hours':req_hours,
                                                                    'bad_users':bad_users})
    else:
        data = Entry.objects.all()
        return render(request, 'registration/search_results.html', {'data': data})
