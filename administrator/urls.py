from django.urls import path
from .views import *

urlpatterns = [
    # path('login/', login_view, name='login'),
    # path('signup/', signup_view, name='signup'),
    # path('dashboard/', dashboard_view, name='dashboard'),
    # path('profile/', profile_view, name='profile'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin-header', header, name='header'),
    path('user_management', user_management, name='user_management'),
    path('citizens', citizens_management, name='citizens_management'),
    path('lawyers', lawyers_management, name='lawyers_management'),
    path('judges', judges_management, name='judges_management'),
    path('case_management', case_management, name='case_management'),
    path('case_status', case_status, name='case_status'),
    path('pending-cases', pending_cases, name='pending_cases'),
    path('active-cases', active_cases, name='active_cases'),
    path('closed-cases', closed_cases, name='closed_cases'),
    path('dismissed-cases', dismissed_cases, name='dismissed_cases'),
    path('all_cases', all_cases, name='all_cases'),
    path('add-judge', add_judge, name='add_judge'),
    path('lawyer-approve-reject', lawyer_approve_reject, name='lawyer_approve_reject'),
    path('approve-reject-lawyer/<str:username>/', approve_or_reject_lawyer, name='approve_or_reject_lawyer'),
    path('profile', profile, name='profile'),
    path('edit-profile', edit_profile, name='edit_profile')
]

handler404 = 'ecourt_home.views.error_404_view'