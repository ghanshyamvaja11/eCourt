from django.urls import path
from .views import *

urlpatterns = [
    path('lawyer-profile', lawyer_profile, name='lawyer_profile'),
    path('lawyer-edit-profile', lawyer_edit_profile, name='lawyer_edit_profile'),
    path('lawyer-dashboard', lawyer_dashboard, name='lawyer_dashboard'),
    path('lawyer-header', header, name='header'),
    path('assigned-cases', assigned_cases, name='assigned_cases'),
    path('hearings', hearings, name='lawyer_hearings'),
    path('efilling', efilling, name='efilling'),
    path('lawyer-profile', lawyer_profile, name='lawyer_profile'),
    path('lawyer-edit-profile', lawyer_edit_profile, name='lawyer_edit_profile'),
    path('plaintiff-case-requests', plaintiff_case_requests, name='plaintiff_case_requests'),
    path('plaintiff-accept-case', plaintiff_accept_case,
         name='plaintiff_accept_case'),
    path('plaintiff-decline-case', plaintiff_decline_case,
         name='plaintiff_decline_case'),
    path('defentdent-case-requests', defendent_case_requests, name='defendent_case_requests'),
    path('defendent-accept-case', defendent_accept_case,
         name='defendent_accept_case'),
    path('defendent-decline-case', defendent_decline_case,
         name='defendent_decline_case'),
    path('logout', logout_view, name='logout'),
    path('notifications', notifications, name='lawyer_notifications'),
]
