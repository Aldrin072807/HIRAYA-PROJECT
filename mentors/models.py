from django.db import models
from django.contrib.auth.models import User

class MentorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    bio = models.TextField(blank=True)
    skills = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mentor: {self.user.username if self.user else 'Unassigned'}"