from django.urls import path
from .views import *

urlpatterns = [
#     path('lawyer-profile', lawyer_profile, name='lawyer_profile'),
#     path('lawyer-edit-profile', lawyer_edit_profile, name='lawyer_edit_profile'),
    path('lawyer-dashboard', lawyer_dashboard, name='lawyer_dashboard'),
    path('lawyer-header', header, name='header'),
    path('assigned-cases', assigned_cases, name='assigned_cases'),
    path('hearings', hearings, name='lawyer_hearings'),
    path('lawyer-profile', lawyer_profile, name='lawyer_profile'),
    path('lawyer-edit-profile', lawyer_edit_profile, name='lawyer_edit_profile'),
    path('plaintiff-case-requests', plaintiff_case_requests, name='plaintiff_case_requests'),
    path('plaintiff-accept-case', plaintiff_accept_case,
         name='plaintiff_accept_case'),
    path('plaintiff-decline-case', plaintiff_decline_case,
         name='plaintiff_decline_case'),
    path('defendent-case-requests', defendant_case_requests, name='defendant_case_requests'),
    path('defendant-accept-case', defendant_accept_case,
         name='defendant_accept_case'),
    path('defendant-decline-case', defendant_decline_case,
         name='defendant_decline_case'),
    path('client-case-docs', client_case_documents, name='client_case_documents'),
    path('request-client-case-documents', request_client_case_documents,
         name='request_client_case_documents'),
    path('logout', logout_view, name='logout'),
    path('notifications', notifications, name='lawyer_notifications'),
    path('request-payment/<int:case_id>/', request_payment, name='request_payment'),
]
