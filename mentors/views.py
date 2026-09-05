from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import MentorProfile
from .forms import MentorProfileForm


def mentor_list(request):
    mentors = MentorProfile.objects.select_related("user").all()
    return render(request, "mentors/mentor_list.html", {"mentors": mentors})


def mentor_detail(request, id):
    mentor = get_object_or_404(MentorProfile.objects.select_related("user"), id=id)
    return render(request, "mentors/mentor_detail.html", {"mentor": mentor})


@login_required
def mentor_create(request):
    if request.method == "POST":
        form = MentorProfileForm(request.POST)
        if form.is_valid():
            mentor = form.save(commit=False)
            mentor.user = request.user
            mentor.save()
            return redirect("mentor_detail", id=mentor.id)
    else:
        form = MentorProfileForm()
    return render(request, "mentors/mentor_form.html", {"form": form})