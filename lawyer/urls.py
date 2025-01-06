from django.urls import path
from .views import *

urlpatterns = [
    path('lawyer-dashboard/', lawyer_dashboard, name='lawyer_dashboard'), 
    path('lawyer-header', header, name='header'), 
    path('assigned-cases', assigned_cases, name='assigned_cases'), 
    path('hearing', hearings, name='hearing'), 
    path('efilling', efilling, name='efilling'), 
    path('lawyer-profile', lawyer_profile, name='lawyer_profile'), 
    path('lawyer-edit-profile', lawyer_edit_profile, name='lawyer_edit_profile'),  
]
