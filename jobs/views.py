from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job, Application
from .forms import JobForm


def get_dashboard_url(user):
    """Returns the appropriate dashboard route based on user privileges."""
    if user.is_authenticated and user.is_staff:
        return 'profiles:admin_dashboard'
    return 'profiles:student_dashboard'


@login_required(login_url='profiles:login')
def job_list(request):
    """
    Shows all available job postings. 
    Accessible to both regular students and staff members.
    """
    jobs = Job.objects.all().order_by('-posted_at')
    dashboard_url = get_dashboard_url(request.user)
    return render(request, 'jobs/job_list.html', {
        'jobs': jobs,
        'dashboard_url': dashboard_url,
    })


def job_detail(request, job_id):
    """Shows details for a single job posting."""
    job = get_object_or_404(Job, id=job_id)
    already_applied = False
    if request.user.is_authenticated:
        already_applied = Application.objects.filter(job=job, applicant=request.user).exists()

    dashboard_url = get_dashboard_url(request.user)
    context = {
        'job': job,
        'already_applied': already_applied,
        'dashboard_url': dashboard_url,
    }
    return render(request, 'jobs/job_detail.html', context)


@login_required(login_url='profiles:login')
def apply_to_job(request, job_id):
    """Creates an Application for the logged-in user, if they haven't already applied."""
    job = get_object_or_404(Job, id=job_id)

    if not Application.objects.filter(job=job, applicant=request.user).exists():
        Application.objects.create(job=job, applicant=request.user)

    return redirect('jobs:job_detail', job_id=job.id)


@login_required(login_url='profiles:login')
def application_history(request):
    """Shows all applications the logged-in user has submitted."""
    applications = Application.objects.filter(applicant=request.user).select_related('job').order_by('-applied_at')
    dashboard_url = get_dashboard_url(request.user)
    return render(request, 'jobs/application_history.html', {
        'applications': applications,
        'dashboard_url': dashboard_url,
    })


@login_required(login_url='profiles:login')
def add_job(request):
    """Staff-only view to add a job posting using custom frontend forms."""
    if not request.user.is_staff:
        return redirect('profiles:student_dashboard')

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profiles:admin_dashboard')
    else:
        form = JobForm()
    
    dashboard_url = get_dashboard_url(request.user)
    return render(request, 'jobs/job_form.html', {
        'form': form, 
        'title': 'Add Job Posting',
        'dashboard_url': dashboard_url,
    })


@login_required(login_url='profiles:login')
def delete_job(request, pk):
    """Staff-only view to delete a job posting."""
    if not request.user.is_staff:
        return redirect('profiles:student_dashboard')

    job = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        job.delete()
        return redirect('profiles:admin_dashboard')
        
    dashboard_url = get_dashboard_url(request.user)
    return render(request, 'jobs/job_confirm_delete.html', {
        'job': job,
        'dashboard_url': dashboard_url,
    })