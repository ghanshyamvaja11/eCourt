from django.shortcuts import render, redirect, get_object_or_404
from users.models import *
from cases.models import *
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import json
from django.db.models import Count
from django.db.models.functions import TruncMonth

# Create your views here.
@login_required(login_url='/login/')
def admin_dashboard(request):
    # Fetch some data to display on the dashboard
    total_users = User.objects.count()
    total_cases = Case.objects.count()
    return render(request, 'admin_dashboard.html', {
        'total_users': total_users,
        'total_cases': total_cases,
    })

@login_required(login_url='/login/')
def header(request):
    return render(request, 'admin_header.html')

@login_required(login_url='/login/')
def user_management(request):
    users = User.objects.all()
    return render(request, 'user_management.html', {'users': users})

@login_required(login_url='/login/')
def citizens_management(request):
    citizens = User.objects.filter(user_type='CITIZEN')
    return render(request, 'citizens_management.html', {'citizens': citizens})

@login_required(login_url='/login/')
def lawyers_management(request):
    lawyers = Lawyer.objects.all()
    return render(request, 'lawyers_management.html', {'lawyers': lawyers})

@login_required(login_url='/login/')
def judges_management(request):
    judges = Judge.objects.all()
    return render(request, 'judges_management.html', {'judges': judges})

@login_required(login_url='/login/')
def case_management(request):
    cases = Case.objects.all()
    return render(request, 'case_management.html', {'cases': cases})

@login_required(login_url='/login/')
def case_status(request):
    cases = Case.objects.all()
    return render(request, 'case_status.html', {'cases': cases})

@login_required(login_url='/login/')
def all_cases(request):
    cases = Case.objects.all()
    return render(request, 'all_cases.html', {'cases': cases})

# Example view for Pending Cases
@login_required(login_url='/login/')
def pending_cases(request):
    cases = Case.objects.filter(status='PENDING')
    return render(request, 'pending_cases.html', {'cases': cases})

# Example view for Active Cases
@login_required(login_url='/login/')
def active_cases(request):
    cases = Case.objects.filter(status='ACTIVE')
    return render(request, 'active_cases.html', {'cases': cases})

# Example view for Closed Cases
@login_required(login_url='/login/')
def closed_cases(request):
    cases = Case.objects.filter(status='CLOSED')
    return render(request, 'closed_cases.html', {'cases': cases})

# Example view for Dismissed Cases
@login_required(login_url='/login/')
def dismissed_cases(request):
    cases = Case.objects.filter(status='DISMISSED')
    return render(request, 'dismissed_cases.html', {'cases': cases})

@login_required(login_url='/login/')
def add_judge(request):
    if request.method == 'POST':
        username = request.POST['username']
        full_name = request.POST['full_name']
        email = request.POST['email']
        contact_number = request.POST['contact_number']
        password = request.POST['password']
        address = request.POST['address']
        allocate_case = request.POST['allocate_case']

        user = User.objects.create_user(username=username, password=password, email=email, full_name=full_name, contact_number=contact_number, address=address, user_type='JUDGE')
        Judge.objects.create(user=user, allocate_case=allocate_case)
        messages.success(request, 'Judge added successfully.')
        return redirect('add_judge')
    return render(request, 'add_judge.html')

@login_required(login_url='/login/')
def lawyer_approve_reject(request):
    lawyers = Lawyer.objects.filter(user__user_type='PENDING_LAWYER')
    return render(request, 'lawyer_request.html', {'lawyers': lawyers})

@login_required(login_url='/login/')
def approve_or_reject_lawyer(request, username):
    user = get_object_or_404(User, username=username)
    try:
        lawyer = Lawyer.objects.get(user=user)
    except Lawyer.DoesNotExist:
        messages.error(request, "This user is not a lawyer.")
        return redirect('admin_dashboard')

    if request.method == "POST":
        action = request.POST.get('action')
        if action == 'approve':
            lawyer.user.user_type = 'LAWYER'
            lawyer.user.is_active = True
            lawyer.user.save()
            messages.success(request, f"Lawyer {user.username} has been approved.")
            # Notify lawyer of approval
            lawyer.user.email_user(
                'Approval Notification',
                'Congratulations, your lawyer account has been approved. now you can login into your account.',
                'ecourtofficially@gmail.com'
            )
        elif action == 'reject':
            lawyer.delete()
            user.delete()
            messages.success(request, f"Lawyer {user.username} has been rejected.")
            # Notify lawyer of rejection
            user.email_user(
                'Rejection Notification',
                'We regret to inform you that your lawyer account has been rejected.',
                'ecourtofficially@gmail.com'
            )
        else:
            messages.error(request, "Invalid action.")
        return redirect('lawyer_approve_reject')

    return render(request, 'approve_reject_lawyer.html', {'lawyer': lawyer})

@login_required(login_url='/login/')
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})

@login_required(login_url='/login/')
def edit_profile(request):
    user = request.user
    # if request.method == 'POST' and user.user_type == 'ADMIN':
    if request.method == 'POST':
        user.username = user.username
        user.full_name = request.POST['full_name']
        user.email = request.POST['email']
        user.contact_number = request.POST['contact_number']
        user.address = request.POST['address']
        if request.FILES.get('profile_image'):
            user.profile_picture = request.FILES['profile_image']
        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')
    return render(request, 'edit_profile.html', {'user': user})

@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout

@login_required(login_url='/login/')
def analytics_dashboard(request):
    # Fetch data for cases
    cases = Case.objects.all()
    case_status_counts = cases.values('status').annotate(count=Count('status'))
    cases_data = {
        'labels': [status['status'] for status in case_status_counts],
        'data': [status['count'] for status in case_status_counts],
        'label': 'Cases'
    }

    # Fetch data for lawyers
    lawyers = Lawyer.objects.all()
    lawyer_case_counts = cases.values('assigned_lawyer__user__full_name').annotate(count=Count('id'))
    lawyers_data = {
        'labels': [lawyer['assigned_lawyer__user__full_name'] for lawyer in lawyer_case_counts],
        'data': [lawyer['count'] for lawyer in lawyer_case_counts],
        'label': 'Cases per Lawyer'
    }

    # Fetch data for judges
    judges = Judge.objects.all()
    judge_case_counts = cases.values('assigned_judge__user__full_name').annotate(count=Count('id'))
    judges_data = {
        'labels': [judge['assigned_judge__user__full_name'] for judge in judge_case_counts],
        'data': [judge['count'] for judge in judge_case_counts],
        'label': 'Cases per Judge'
    }

    # Fetch data for citizens
    citizens = Citizen.objects.all()
    citizens_data = {
        'labels': ['Total Citizens'],
        'data': [citizens.count()],
        'label': 'Citizens'
    }

    # Fetch data for case types
    case_types = cases.values('case_type').annotate(count=Count('case_type'))
    case_types_data = {
        'labels': [case_type['case_type'] for case_type in case_types],
        'data': [case_type['count'] for case_type in case_types],
        'label': 'Case Types'
    }

    # Fetch data for monthly cases
    monthly_cases = cases.annotate(month=TruncMonth('case_filed_date')).values('month').annotate(count=Count('id')).order_by('month')
    monthly_cases_data = {
        'labels': [month['month'].strftime('%B %Y') for month in monthly_cases],
        'data': [month['count'] for month in monthly_cases],
        'label': 'Monthly Cases'
    }

    # Fetch data for hearings
    hearings = Hearing.objects.all()
    hearing_counts = hearings.values('date').annotate(count=Count('id'))
    hearings_data = {
        'labels': [hearing['date'].strftime('%Y-%m-%d') for hearing in hearing_counts],
        'data': [hearing['count'] for hearing in hearing_counts],
        'label': 'Hearings'
    }

    # Fetch data for documents
    documents = Document.objects.all()
    document_counts = documents.values('document_type').annotate(count=Count('id'))
    documents_data = {
        'labels': [document['document_type'] for document in document_counts],
        'data': [document['count'] for document in document_counts],
        'label': 'Documents'
    }

    context = {
        'cases_data': json.dumps(cases_data),
        'lawyers_data': json.dumps(lawyers_data),
        'judges_data': json.dumps(judges_data),
        'citizens_data': json.dumps(citizens_data),
        'case_types_data': json.dumps(case_types_data),
        'monthly_cases_data': json.dumps(monthly_cases_data),
        'hearings_data': json.dumps(hearings_data),
        'documents_data': json.dumps(documents_data)
    }

    return render(request, 'analytics.html', context)

@login_required(login_url='/login/')
def reports_dashboard(request):
    # Fetch data for cases
    cases = Case.objects.all()
    case_status_counts = cases.values('status').annotate(count=Count('status'))
    cases_data = {
        'labels': [status['status'] for status in case_status_counts],
        'data': [status['count'] for status in case_status_counts],
        'label': 'Cases'
    }

    # Fetch data for lawyers
    lawyers = Lawyer.objects.all()
    lawyer_case_counts = cases.values('assigned_lawyer__user__full_name').annotate(count=Count('id'))
    lawyers_data = {
        'labels': [lawyer['assigned_lawyer__user__full_name'] for lawyer in lawyer_case_counts],
        'data': [lawyer['count'] for lawyer in lawyer_case_counts],
        'label': 'Cases per Lawyer'
    }

    # Fetch data for judges
    judges = Judge.objects.all()
    judge_case_counts = cases.values('assigned_judge__user__full_name').annotate(count=Count('id'))
    judges_data = {
        'labels': [judge['assigned_judge__user__full_name'] for judge in judge_case_counts],
        'data': [judge['count'] for judge in judge_case_counts],
        'label': 'Cases per Judge'
    }

    # Fetch data for citizens
    citizens = Citizen.objects.all()
    citizens_data = {
        'labels': ['Total Citizens'],
        'data': [citizens.count()],
        'label': 'Citizens'
    }

    # Fetch data for case types
    case_types = cases.values('case_type').annotate(count=Count('case_type'))
    case_types_data = {
        'labels': [case_type['case_type'] for case_type in case_types],
        'data': [case_type['count'] for case_type in case_types],
        'label': 'Case Types'
    }

    # Fetch data for monthly cases
    monthly_cases = cases.annotate(month=TruncMonth('case_filed_date')).values('month').annotate(count=Count('id')).order_by('month')
    monthly_cases_data = {
        'labels': [month['month'].strftime('%B %Y') for month in monthly_cases],
        'data': [month['count'] for month in monthly_cases],
        'label': 'Monthly Cases'
    }

    # Fetch data for hearings
    hearings = Hearing.objects.all()
    hearing_counts = hearings.values('date').annotate(count=Count('id'))
    hearings_data = {
        'labels': [hearing['date'].strftime('%Y-%m-%d') for hearing in hearing_counts],
        'data': [hearing['count'] for hearing in hearing_counts],
        'label': 'Hearings'
    }

    # Fetch data for documents
    documents = Document.objects.all()
    document_counts = documents.values('document_type').annotate(count=Count('id'))
    documents_data = {
        'labels': [document['document_type'] for document in document_counts],
        'data': [document['count'] for document in document_counts],
        'label': 'Documents'
    }

    context = {
        'cases_data': json.dumps(cases_data),
        'lawyers_data': json.dumps(lawyers_data),
        'judges_data': json.dumps(judges_data),
        'citizens_data': json.dumps(citizens_data),
        'case_types_data': json.dumps(case_types_data),
        'monthly_cases_data': json.dumps(monthly_cases_data),
        'hearings_data': json.dumps(hearings_data),
        'documents_data': json.dumps(documents_data)
    }

    return render(request, 'administrator/reports.html', context)
