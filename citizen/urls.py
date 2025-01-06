from django.urls import path
from .views import *

urlpatterns = [
    path('citizen-dashboard/', citizen_dashboard, name='citizen_dashboard'),
    path('citizen-header', header, name='header'),
    path('file-cases', file_cases, name='file_cases'),
    path('my-cases', my_cases, name='my_cases'),
    path('efilling', efilling, name='efilling'),
    path('notification', notification, name='notification'),
    path('citizen-profile', citizen_profile, name='citizen_profile'),
    path('citizen-edit-profile', citizen_edit_profile, name='citizen_edit_profile'),
]
