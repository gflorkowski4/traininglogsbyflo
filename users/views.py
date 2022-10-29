from urllib import response
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.db.models.functions import Extract
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from training_logs.models import Entry, Topic
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from training_logs.models import Profile
from .forms import EditUserForm, SignUpForm, EditProfileForm
import csv
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
            new_profile = Profile.objects.create(user=request.user)
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
    style_percent = total_hours[request.user]/12*100
    return render(request, 'registration/dashboard.html',
                  {'entries': entries,
                   'topics': topics,
                   'users': users,
                   'owner': owner,
                   'total_hours': total_hours,
                   'current_month': current_month,
                   'style_percent':style_percent})


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

        for method in ['TSE', 'Remote', 'Class', 'In Flight', 'Self Study','DSE','CSPT','Global','CMCT','OPI','DLPT']:
            method_hours = 0
            for entry in entries:
                if entry.month_published() == current_month:
                    if entry.method_of_training == method:
                        method_hours += entry.hours
            training_method_hours[method] = method_hours

        

        x_data = [0,1,2,3]
        y_data = [x**2 for x in x_data]
        plt_div = plot([Scatter(x=x_data, y=y_data,
                        mode='lines', name='test',
                        opacity=0.8, marker_color='green')],
                        output_type='div')


        return render(request, 'registration/admin_dashboard.html',
                      {'entries': entries,
                       'topics': topics,
                       'users': users,
                       'owner': owner,
                       'total_hours': total_hours,
                       'training_method_hours': training_method_hours,
                       'current_month': current_month,
                       'plt_div':plt_div,})
    else:
        raise Http404

# EDIT PROFILE =====================================================================================
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditUserForm(request.POST or None, instance=request.user)
        form_2 = EditProfileForm(request.POST or None, instance=request.user.profile)
        if all([form.is_valid(),form_2.is_valid()]):
            parent = form.save(commit=False)
            parent.save()
            child = form_2.save(commit=False)
            child.User = parent
            child.save()
            return redirect('users:dashboard')
    else:
        form = EditUserForm(instance=request.user)
        form_2 = EditProfileForm(instance=request.user)
        args = {
            'form': form,
            'form_2':form_2}
        return render(request, 'registration/edit_profile.html', args)

# SEARCH RESULTS
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


        data = Entry.objects.filter(
            date_training_conducted__range=(start_date, end_date)).order_by('-date_training_conducted')

        # Query for Each Training Method Totals
        for method in ['TSE', 'Remote', 'Class', 'In Flight', 'Self Study','DSE','CSPT','Global','CMCT','OPI','DLPT']:
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

@login_required
def password_change(request):
    return render(request, 'registration/password_changed.html',{})


def results_csv(request):
    #find a way to pull the same information and pull the dates as well
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=results.csv'
    data = Entry.objects.all()

    #CSV Writer 
    writer = csv.writer(response)
    # Model
    data = Entry.objects.all()

    writer.writerow(['Student Name','Role','Topic','Method of Training', 'Date Training Conducted', 'Training Hours'])

    for entry in data:
        writer.writerow([entry.topic.owner.first_name+' '+entry.topic.owner.last_name,entry.topic.owner.profile.role,entry.topic.text,
        entry.method_of_training, entry.date_training_conducted, entry.hours])

    return response



    
