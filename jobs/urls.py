from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    # Student pages
    path('', views.job_list, name='job_list'),
    path('my-applications/', views.application_history, name='application_history'),

    # Admin application management
    path(
        'applications/',
        views.admin_application_list,
        name='admin_application_list'
    ),
    path(
        'applications/<int:application_id>/',
        views.admin_application_detail,
        name='admin_application_detail'
    ),
    path(
        'applications/<int:application_id>/accept/',
        views.accept_application,
        name='accept_application'
    ),
    path(
        'applications/<int:application_id>/reject/',
        views.reject_application,
        name='reject_application'
    ),

    # Admin job management
    path('add/', views.add_job, name='add_job'),
    path('delete/<int:pk>/', views.delete_job, name='delete_job'),

    # Job details
    path('<int:job_id>/', views.job_detail, name='job_detail'),
    path('<int:job_id>/apply/', views.apply_to_job, name='apply_to_job'),
]