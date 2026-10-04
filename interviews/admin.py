from django.contrib import admin
from .models import Question, InterviewSession, AnswerSubmission

admin.site.register(Question)
admin.site.register(InterviewSession)
admin.site.register(AnswerSubmission)