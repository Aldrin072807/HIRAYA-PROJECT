from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job, Application
from .forms import JobForm


def get_dashboard_url(user):
    """Returns the appropriate dashboard route based on user privileges."""
    if user.is_authenticated and user.is_staff:
        return 'profiles:admin_dashboard'
    return 'profiles:dashboard'


@login_required(login_url='profiles:login')
def job_list(request):
    """Shows all available job postings."""
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
        already_applied = Application.objects.filter(
            job=job,
            applicant=request.user
        ).exists()

    dashboard_url = get_dashboard_url(request.user)

    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'already_applied': already_applied,
        'dashboard_url': dashboard_url,
    })


@login_required(login_url='profiles:login')
def apply_to_job(request, job_id):
    """Creates a pending application for the logged-in student."""
    job = get_object_or_404(Job, id=job_id)

    if not Application.objects.filter(
        job=job,
        applicant=request.user
    ).exists():

        Application.objects.create(
            job=job,
            applicant=request.user,
            status='pending'
        )

    return redirect('jobs:job_detail', job_id=job.id)


@login_required(login_url='profiles:login')
def application_history(request):
    """Shows the student's submitted applications and their status."""
    applications = Application.objects.filter(
        applicant=request.user
    ).select_related('job').order_by('-applied_at')

    dashboard_url = get_dashboard_url(request.user)

    return render(request, 'jobs/application_history.html', {
        'applications': applications,
        'dashboard_url': dashboard_url,
    })


# =========================================================
# ADMIN APPLICATION MANAGEMENT
# =========================================================

@login_required(login_url='profiles:login')
def admin_application_list(request):
    """Shows all job applications to staff members."""
    if not request.user.is_staff:
        return redirect('profiles:dashboard')

    applications = Application.objects.select_related(
        'job',
        'applicant'
    ).order_by('-applied_at')

    return render(request, 'jobs/admin_application_list.html', {
        'applications': applications,
        'dashboard_url': 'profiles:admin_dashboard',
    })


@login_required(login_url='profiles:login')
def admin_application_detail(request, application_id):
    """Shows the applicant's information to staff members."""
    if not request.user.is_staff:
        return redirect('profiles:dashboard')

    application = get_object_or_404(
        Application.objects.select_related(
            'job',
            'applicant'
        ),
        id=application_id
    )

    # Get the student's profile if it exists
    profile = getattr(application.applicant, 'userprofile', None)

    return render(request, 'jobs/admin_application_detail.html', {
        'application': application,
        'profile': profile,
        'dashboard_url': 'profiles:admin_dashboard',
    })


@login_required(login_url='profiles:login')
def accept_application(request, application_id):
    """Allows staff to accept an application."""
    if not request.user.is_staff:
        return redirect('profiles:dashboard')

    application = get_object_or_404(
        Application,
        id=application_id
    )

    if request.method == 'POST':
        application.status = 'accepted'
        application.save()

    return redirect(
        'jobs:admin_application_detail',
        application_id=application.id
    )


@login_required(login_url='profiles:login')
def reject_application(request, application_id):
    """Allows staff to reject an application."""
    if not request.user.is_staff:
        return redirect('profiles:dashboard')

    application = get_object_or_404(
        Application,
        id=application_id
    )

    if request.method == 'POST':
        application.status = 'rejected'
        application.save()

    return redirect(
        'jobs:admin_application_detail',
        application_id=application.id
    )


# =========================================================
# ADMIN JOB MANAGEMENT
# =========================================================

@login_required(login_url='profiles:login')
def add_job(request):
    """Staff-only view to add a job posting."""
    if not request.user.is_staff:
        return redirect('profiles:dashboard')

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
        return redirect('profiles:dashboard')

    job = get_object_or_404(Job, pk=pk)

    if request.method == 'POST':
        job.delete()
        return redirect('profiles:admin_dashboard')

    dashboard_url = get_dashboard_url(request.user)

    return render(request, 'jobs/job_confirm_delete.html', {
        'job': job,
        'dashboard_url': dashboard_url,
    })