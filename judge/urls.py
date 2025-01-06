from django.urls import path
from .views import *

urlpatterns = [
    path('judge-dashboard/', judge_dashboard, name='judge_dashboard'),
    path('judge-assigned-cases/', judge_assigned_cases, name='judge_assigned_cases'),
    path('judge-hearing/', judge_hearing, name='judge_hearing'),
    path('outcome/', outcome, name='outcome'),
    path('case-doc/', case_doc, name='case_doc'),
    path('judge-profile/', judge_profile, name='judge_profile'),
    path('judge-edit-profile/', judge_edit_profile, name='judge_edit_profile'),
]