from django.urls import path
from .views import *

urlpatterns = [
    path('citizen-dashboard', citizen_dashboard, name='citizen_dashboard'),
    path('citizen-header', header, name='header'),
    path('file-cases', file_cases, name='file_cases'),
    path('my-cases', my_cases, name='my_cases'),
    path('efilling', efilling, name='efilling'),
    path('notification', notification, name='notification'),
    path('logout/', logout_view, name='logout'),
    path('documents/', case_documents, name='case_documents'),
    path('notifications/', notifications, name='notifications'),
    path('against-cases', against_cases, name='against_cases'),
    path('profile/', profile, name='profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
]
