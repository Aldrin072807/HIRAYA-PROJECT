from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import MentorProfile
from .forms import MentorForm

def mentor_list(request):
    """Displays all mentor profiles."""
    mentors = MentorProfile.objects.all()
    return render(request, 'mentors/mentor_list.html', {'mentors': mentors})

def mentor_detail(request, id):
    """Displays a single mentor profile."""
    mentor = get_object_or_404(MentorProfile, id=id)
    return render(request, 'mentors/mentor_detail.html', {'mentor': mentor})

@staff_member_required
def add_mentor(request):
    """Staff-only view to create a new mentor entry from the custom dashboard."""
    if request.method == 'POST':
        form = MentorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profiles:admin_dashboard')
    else:
        form = MentorForm()
    return render(request, 'mentors/mentor_form.html', {'form': form, 'title': 'Add Mentor Profile'})

@staff_member_required
def delete_mentor(request, pk):
    """Staff-only view to remove a mentor entry."""
    mentor = get_object_or_404(MentorProfile, pk=pk)
    if request.method == 'POST':
        mentor.delete()
        return redirect('profiles:admin_dashboard')
    return render(request, 'jobs/job_confirm_delete.html', {'object': mentor})