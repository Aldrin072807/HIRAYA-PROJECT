from django import forms
from .models import MentorProfile

class MentorForm(forms.ModelForm):
    class Meta:
        model = MentorProfile
        fields = '__all__'