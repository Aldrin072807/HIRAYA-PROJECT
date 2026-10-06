from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.apps import apps

from .forms import UserRegisterForm
from .models import UserProfile


def get_safe_model(app_label, model_names):
    """Safely retrieves a model by trying a list of possible model names."""
    for model_name in model_names:
        try:
            return apps.get_model(app_label, model_name)
        except LookupError:
            continue
    return None


def register(request):
    """Registers standard members and routes them directly to the Student Dashboard."""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profiles:dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'profiles/register.html', {'form': form})


def custom_login(request):
    """
    Handles role-based authentication routing:
    - Admin/Staff Users -> Custom Admin Control Board
    - Regular Members -> Student Dashboard
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff or user.is_superuser:
                return redirect('profiles:admin_dashboard')
            return redirect('profiles:dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'profiles/login.html', {'form': form})


@login_required
def student_dashboard(request):
    """Renders the main student dashboard hub."""
    profile, created = UserProfile.objects.get_or_create(user=request.user) if hasattr(request.user, 'userprofile') else (None, False)
    
    ApplicationModel = get_safe_model('jobs', ['Application', 'JobApplication'])
    InterviewModel = get_safe_model('interviews', ['InterviewSession', 'Session', 'Interview'])

    recent_applications = ApplicationModel.objects.filter(applicant=request.user).order_by('-applied_at')[:3] if ApplicationModel else []
    recent_interviews = InterviewModel.objects.filter(user=request.user).order_by('-started_at')[:3] if InterviewModel else []

    context = {
        'profile': profile,
        'recent_applications': recent_applications,
        'recent_interviews': recent_interviews,
    }
    return render(request, 'profiles/dashboard.html', context)


@staff_member_required
def admin_dashboard(request):
    """Renders the custom administrative control panel for staff members."""
    JobModel = get_safe_model('jobs', ['Job', 'JobPosting'])
    ApplicationModel = get_safe_model('jobs', ['Application', 'JobApplication'])
    MentorModel = get_safe_model('mentors', ['MentorProfile', 'Mentor'])

    total_jobs = JobModel.objects.count() if JobModel else 0
    total_applications = ApplicationModel.objects.count() if ApplicationModel else 0
    total_mentors = MentorModel.objects.count() if MentorModel else 0
    recent_apps = ApplicationModel.objects.order_by('-applied_at')[:5] if ApplicationModel else []

    context = {
        'total_jobs': total_jobs,
        'total_applications': total_applications,
        'total_mentors': total_mentors,
        'recent_applications': recent_apps,
    }
    return render(request, 'profiles/admin_dashboard.html', context)