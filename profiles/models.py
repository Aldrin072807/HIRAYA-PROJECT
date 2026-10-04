from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    skills = models.TextField(help_text="List your skills separated by commas")
    experience = models.TextField(help_text="Describe your work experience or background")
    career_interests = models.CharField(max_length=255, help_text="Your target field or career interests")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"