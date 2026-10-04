from django.db import models
from django.contrib.auth.models import User


class MentorProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="mentor_profile"
    )
    bio = models.TextField(blank=True)
    expertise = models.TextField(help_text="Enter skills separated by commas.")
    experience = models.TextField(blank=True)
    career_field = models.CharField(max_length=100)
    availability = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username