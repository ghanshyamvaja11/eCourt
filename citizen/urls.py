from django.urls import path
from .views import *

urlpatterns = [
    path('citizen-dashboard', citizen_dashboard, name='citizen_dashboard'),
    path('citizen-header', header, name='header'),
    path('file-cases', file_cases, name='file_cases'),
    path('my-cases', my_cases, name='my_cases'),
    path('citizen-efilling', citizen_efilling, name='citizen_efilling'),
    path('notifications', notifications, name='notifications'),
    path('logout', logout_view, name='logout'),
    path('documents', case_documents, name='case_documents'),
    path('hearings', hearings, name='citizen_hearings'),
    path('notifications', notifications, name='notifications'),
    path('against-cases', against_cases, name='against_cases'),
    path('citizen-profile', citizen_profile, name='citizen_profile'),
    path('citizen-edit-profile', citizen_edit_profile, name='citizen_edit_profile'),
]
