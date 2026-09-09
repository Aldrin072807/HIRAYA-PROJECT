from django.contrib import admin
from django.urls import path, include
from interviews.views import start_interview

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', start_interview, name='home'),
    path('profiles/', include('profiles.urls')),
    path('interviews/', include('interviews.urls')),
]