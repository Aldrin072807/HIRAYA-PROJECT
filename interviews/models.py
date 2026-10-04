from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    category = models.CharField(max_length=100)  # e.g., "Behavioral", "Technical", "Django"
    text = models.TextField()
    time_limit_seconds = models.IntegerField(default=120)  # Timer duration per question
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.category}] {self.text[:50]}"


class InterviewSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interview_sessions')
    started_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Session {self.id} - {self.user.username}"


class AnswerSubmission(models.Model):
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_answer = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(null=True, blank=True)  # Reserved for manual or AI feedback
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Answer for {self.question.id} in Session {self.session.id}"