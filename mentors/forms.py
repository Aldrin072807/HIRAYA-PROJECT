from django import forms
from .models import MentorProfile


class MentorProfileForm(forms.ModelForm):
    class Meta:
        model = MentorProfile
        fields = ["bio", "expertise", "experience", "career_field", "availability"]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4, "placeholder": "Tell students about yourself..."}),
            "expertise": forms.TextInput(attrs={"placeholder": "Python, Django, Web Development"}),
            "experience": forms.Textarea(attrs={"rows": 4, "placeholder": "Describe your professional experience..."}),
            "career_field": forms.TextInput(attrs={"placeholder": "Software Development"}),
            "availability": forms.TextInput(attrs={"placeholder": "Weekends, 2:00 PM - 5:00 PM"}),
        }