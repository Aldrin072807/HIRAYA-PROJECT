from django.contrib import admin
from django.urls import path, include
from landing.views import index as landing_index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_index, name='home'),
    path('mentors/', include('mentors.urls')),
    path('profiles/', include('profiles.urls')),
    path('interviews/', include('interviews.urls')),
    path('jobs/', include('jobs.urls')),
]