from django.urls import path
from . import views

urlpatterns = [
    path('', views.mentor_list, name='mentor_list'),
    path('<int:id>/', views.mentor_detail, name='mentor_detail'),
    path('add/', views.add_mentor, name='add_mentor'),
    path('<int:pk>/delete/', views.delete_mentor, name='delete_mentor'),
]