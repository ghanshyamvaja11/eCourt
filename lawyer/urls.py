from django.urls import path
from .views import *

urlpatterns = [
    path('lawyer-dashboard/', lawyer_dashboard, name='lawyer_dashboard'),
    path('lawyer-header', header, name='header'),
    path('assigned-cases', assigned_cases, name='assigned_cases'),
    path('hearings', hearings, name='hearings'),
    path('efilling', efilling, name='efilling'),
    path('lawyer-profile', lawyer_profile, name='lawyer_profile'),
    path('lawyer-edit-profile', lawyer_edit_profile, name='lawyer_edit_profile'),
    path('case-requests/', case_requests, name='case_requests'),
    path('accept-case/', accept_case, name='accept_case'),
    path('decline-case/', decline_case, name='decline_case'),
    path('logout/', logout_view, name='logout'),
    path('notifications/', notifications, name='notifications'),
    path('client_case_documents/', client_case_documents, name='client_case_documents'),
]
