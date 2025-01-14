from django.urls import path
from .views import *

urlpatterns = [
   path('judge-dashboard', judge_dashboard, name='judge_dashboard'),
   path('judge-assigned-cases', judge_assigned_cases, name='judge_assigned_cases'),
   path('update-case-status/', update_case_status, name='update_case_status'),
   path('judge-hearing', judge_hearing, name='judge_hearing'),
   path('outcome', outcome, name='outcome'),
   path('case-doc', case_doc, name='case_doc'),
   path('judge-profile', judge_profile, name='judge_profile'),
   path('judge-edit-profile', judge_edit_profile, name='judge_edit_profile'),
   path('logout', logout_view, name='logout'),
   path('schedule-hearing', schedule_hearing, name='schedule_hearing'),
   path('notifications', notifications, name='judge_notifications'),
]