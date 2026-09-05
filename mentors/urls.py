from django.urls import path
from . import views

urlpatterns = [
    path("", views.mentor_list, name="mentor_list"),
    path("<int:id>/", views.mentor_detail, name="mentor_detail"),
    path("create/", views.mentor_create, name="mentor_create"),
]