from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    YEAR_LEVEL_CHOICES = [
        ('1st Year', '1st Year'),
        ('2nd Year', '2nd Year'),
        ('3rd Year', '3rd Year'),
        ('4th Year', '4th Year'),
        ('5th Year', '5th Year'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    program = models.CharField(
        max_length=150,
        blank=True,
        help_text="Your course or academic program"
    )

    year_level = models.CharField(
        max_length=20,
        choices=YEAR_LEVEL_CHOICES,
        blank=True
    )

    bio = models.TextField(
        blank=True,
        null=True
    )

    skills = models.TextField(
        blank=True,
        help_text="List your skills separated by commas"
    )

    experience = models.TextField(
        blank=True,
        help_text="Describe your work experience, projects, or background"
    )

    career_interests = models.CharField(
        max_length=255,
        blank=True,
        help_text="Your target field or career interests"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"