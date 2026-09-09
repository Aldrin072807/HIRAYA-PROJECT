from django.urls import path
from . import views

app_name = 'interviews'

urlpatterns = [
    path('', views.start_interview, name='start_interview'),
    path('session/<int:session_id>/question/<int:question_id>/', views.interview_question, name='interview_question'),
    path('session/<int:session_id>/results/', views.interview_results, name='interview_results'),
]
