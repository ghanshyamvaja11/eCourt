from django.urls import path
from . import views

urlpatterns = [
    path('admin-dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('admin-header', views.header, name='header'),
    path('user-management', views.user_management, name='user_management'),
    path('citizens-management', views.citizens_management, name='citizens_management'),
    path('lawyers-management', views.lawyers_management, name='lawyers_management'),
    path('judges-management', views.judges_management, name='judges_management'),
    path('case-management', views.case_management, name='case_management'),
    path('case-status', views.case_status, name='case_status'),
    path('all-cases', views.all_cases, name='all_cases'),
    path('pending-cases', views.pending_cases, name='pending_cases'),
    path('active-cases', views.active_cases, name='active_cases'),
    path('closed-cases', views.closed_cases, name='closed_cases'),
    path('dismissed-cases', views.dismissed_cases, name='dismissed_cases'),
    path('add-judge', views.add_judge, name='add_judge'),
    path('lawyer-approve-reject', views.lawyer_approve_reject, name='lawyer_approve_reject'),
    path('approve-or-reject-lawyer/<str:username>', views.approve_or_reject_lawyer, name='approve_or_reject_lawyer'),
    path('profile', views.profile, name='profile'),
    path('edit-profile', views.edit_profile, name='edit_profile'),
    path('logout', views.logout_view, name='logout'),
    path('analytics-dashboard', views.analytics_dashboard, name='analytics_dashboard'),
    path('reports-dashboard', views.reports_dashboard, name='reports_dashboard'),
]

handler404 = 'ecourt_home.views.error_404_view'