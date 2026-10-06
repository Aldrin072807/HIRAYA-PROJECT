from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('<int:job_id>/', views.job_detail, name='job_detail'),
    path('<int:job_id>/apply/', views.apply_to_job, name='apply_to_job'),
    path('my-applications/', views.application_history, name='application_history'),
    path('add/', views.add_job, name='add_job'),
    path('delete/<int:pk>/', views.delete_job, name='delete_job'),
]