from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import MentorProfile
from .forms import MentorProfileForm
from profiles.models import UserProfile
from .matching import calculate_match


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

@login_required
def mentor_recommendations(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    mentors = MentorProfile.objects.select_related("user").all()

    recommendations = []
    for mentor in mentors:
        score = calculate_match(user_profile, mentor)
        recommendations.append({"mentor": mentor, "score": score})

    recommendations.sort(key=lambda item: item["score"], reverse=True)

    return render(request, "mentors/mentor_recommendations.html", {
        "recommendations": recommendations
    })