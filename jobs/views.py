from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job, Application

def job_list(request):
    """Shows all available job postings."""
    jobs = Job.objects.all().order_by('-posted_at')
    return render(request, 'jobs/job_list.html', {'jobs': jobs})


def job_detail(request, job_id):
    """Shows details for a single job posting."""
    job = get_object_or_404(Job, id=job_id)
    already_applied = False
    if request.user.is_authenticated:
        already_applied = Application.objects.filter(job=job, applicant=request.user).exists()

    context = {
        'job': job,
        'already_applied': already_applied,
    }
    return render(request, 'jobs/job_detail.html', context)


@login_required
def apply_to_job(request, job_id):
    """Creates an Application for the logged-in user, if they haven't already applied."""
    job = get_object_or_404(Job, id=job_id)

    if not Application.objects.filter(job=job, applicant=request.user).exists():
        Application.objects.create(job=job, applicant=request.user)

    return redirect('jobs:job_detail', job_id=job.id)


@login_required
def application_history(request):
    """Shows all applications the logged-in user has submitted."""
    applications = Application.objects.filter(applicant=request.user).select_related('job').order_by('-applied_at')
    return render(request, 'jobs/application_history.html', {'applications': applications})

# Create your views here.
