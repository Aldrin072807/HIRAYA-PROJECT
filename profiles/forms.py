from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class UserRegisterForm(forms.ModelForm):
    # Account information
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your first name'})
    )

    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your last name'})
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email address'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter password'
        })
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm password'
        })
    )

    # Student profile information
    program = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g. BS Computer Engineering'
        })
    )

    year_level = forms.ChoiceField(
        required=True,
        choices=UserProfile.YEAR_LEVEL_CHOICES
    )

    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Tell us a little about yourself',
            'rows': 3
        })
    )

    skills = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'placeholder': 'e.g. Python, Django, C++, HTML/CSS',
            'rows': 3
        })
    )

    experience = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Projects, work experience, organizations, etc.',
            'rows': 3
        })
    )

    career_interests = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g. Software Engineering'
        })
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "An account with this email address already exists."
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error(
                'confirm_password',
                "Passwords do not match."
            )

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        email = self.cleaned_data['email']

        # Generate username automatically from email
        base_username = email.split('@')[0]
        username = base_username
        counter = 1

        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user.username = username
        user.email = email
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

            UserProfile.objects.create(
                user=user,
                program=self.cleaned_data['program'],
                year_level=self.cleaned_data['year_level'],
                bio=self.cleaned_data.get('bio', ''),
                skills=self.cleaned_data['skills'],
                experience=self.cleaned_data.get('experience', ''),
                career_interests=self.cleaned_data['career_interests']
            )

        return user