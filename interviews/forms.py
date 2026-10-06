from django import forms
from .models import Question

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['category', 'question_text', 'sample_answer']
        widgets = {
            'category': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., Technical, Behavioral'}),
            'question_text': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Enter interview question...'}),
            'sample_answer': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Expected answer guidelines...'}),
        }