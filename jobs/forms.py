from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company', 'location', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., Software Engineer'}),
            'company': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., Tech Solutions Inc.'}),
            'location': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., Clark, Pampanga'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Job description and requirements...'}),
        }