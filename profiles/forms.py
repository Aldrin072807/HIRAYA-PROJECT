from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    skills = forms.CharField(widget=forms.Textarea, help_text="List your skills separated by commas")
    experience = forms.CharField(widget=forms.Textarea, help_text="Describe your work experience or background")
    career_interests = forms.CharField(max_length=255, help_text="Your target field or career interests")

    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'skills', 'experience', 'career_interests']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            
            UserProfile.objects.create(
                user=user,
                bio=self.cleaned_data.get('bio'),
                skills=self.cleaned_data.get('skills'),
                experience=self.cleaned_data.get('experience'),
                career_interests=self.cleaned_data.get('career_interests')
            )
        return user