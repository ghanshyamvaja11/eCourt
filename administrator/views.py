from django.shortcuts import render, redirect, get_object_or_404
from users.models import *
from cases.models import *
from .models import ContactUs
from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.conf import settings
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
def citizens_management(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        reason = request.POST.get('reason')
        citizen = get_object_or_404(Citizen, user_id=user_id)
        user = citizen.user
        citizen.delete()
        user.email_user(
            'Account Deletion Notification',
            f'Your account has been deleted for the following reason: {reason}',
            'ecourtofficially@gmail.com'
        )
        messages.success(request, 'Citizen deleted successfully.')
        return redirect('citizens_management')

    citizens = Citizen.objects.all()
    return render(request, 'citizens_management.html', {'citizens': citizens})

@login_required(login_url='/login/')
def lawyers_management(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        reason = request.POST.get('reason')
        lawyer = get_object_or_404(Lawyer, user_id=user_id)
        user = lawyer.user
        lawyer.delete()
        user.email_user(
            'Account Deletion Notification',
            f'Your account has been deleted for the following reason: {reason}',
            'ecourtofficially@gmail.com'
        )
        messages.success(request, 'Lawyer deleted successfully.')
        return redirect('lawyers_management')

    lawyers = Lawyer.objects.all()
    return render(request, 'lawyers_management.html', {'lawyers': lawyers})

@login_required(login_url='/login/')
def judges_management(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        reason = request.POST.get('reason')
        judge = get_object_or_404(Judge, user_id=user_id)
        user = judge.user
        judge.delete()
        user.email_user(
            'Account Deletion Notification',
            f'Your account has been deleted for the following reason: {reason}',
            'ecourtofficially@gmail.com'
        )
        messages.success(request, 'Judge deleted successfully.')
        return redirect('judges_management')

    judges = Judge.objects.all()
    return render(request, 'judges_management.html', {'judges': judges})

@login_required(login_url='/login/')
def case_management(request):
    if request.method == 'POST':
        case_id = request.POST.get('case_id')
        reason = request.POST.get('reason')
        case = get_object_or_404(Case, id=case_id)
        case.delete()
        # Assuming the case has a related user to notify
        user = case.user
        user.email_user(
            'Case Deletion Notification',
            f'Your case has been deleted for the following reason: {reason}',
            'ecourtofficially@gmail.com'
        )
        messages.success(request, 'Case deleted successfully.')
        return redirect('case_management')

    cases = Case.objects.all()
    return render(request, 'cases_management.html', {'cases': cases})

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
        court = request.POST['court']

        user = User.objects.create_user(username=username, password=password, email=email, full_name=full_name, contact_number=contact_number, address=address, user_type='JUDGE')
        Judge.objects.create(user=user, court=court)
        messages.success(request, 'Judge added successfully.')
        send_mail(
            'Judge Registration',
            f'You have been registered as a judge with the following details:\n\n'
            f'Username: {username}\n Password: {password} \n Full Name: {full_name}\n Email: {email} \n Contact Number: {contact_number}\n Address: {address}\n Allocated Court: {court}\n'
            f'Please log in to your account to start using the system.',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return redirect('add_judge')
    return render(request, 'add_judge.html')

@login_required(login_url='/login/')
def lawyer_approve_reject(request):
    lawyers = Lawyer.objects.filter(user__is_active=False)
    return render(request, 'lawyer_requests.html', {'lawyers': lawyers})

@login_required(login_url='/login/')
def lawyer_approve(request):
    user = get_object_or_404(User, username=request.GET['username'])
    try:
        lawyer = Lawyer.objects.get(user=user)
    except Lawyer.DoesNotExist:
        messages.error(request, "This user is not a lawyer.")
        return redirect('admin_dashboard')
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

    return render(request, 'lawyer_requests.html', {'lawyer': lawyer})


@login_required(login_url='/login/')
def lawyer_reject(request):
    user = get_object_or_404(User, username=request.GET['username'])
    try:
        lawyer = Lawyer.objects.get(user=user)
    except Lawyer.DoesNotExist:
        messages.error(request, "This user is not a lawyer.")
        return redirect('admin_dashboard')

        
    lawyer.delete()
    messages.success(
        request, f"Lawyer {user.username} has been rejected.")
    # Notify lawyer of rejection
    user.email_user(
        'Rejection Notification',
        'We regret to inform you that your lawyer account has been rejected.',
        'ecourtofficially@gmail.com'
    )

    return render(request, 'lawyer_requests.html', {'lawyer': lawyer})

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

    return render(request, 'reports.html', context)

@login_required(login_url='/login/')
def contact_us_reply(request):
    # Clear all previous messages
    storage = messages.get_messages(request)
    storage.used = True

    if request.method == 'POST':
        contact_id = request.POST.get('contact_id')
        reply_message = request.POST.get('reply_message')
        contact = get_object_or_404(ContactUs, id=contact_id)
        contact.delete()
        
        # Send email to the user with the reply message
        send_mail(
            f'Reply to Your Query: {contact.subject}',
            reply_message,
            settings.DEFAULT_FROM_EMAIL,
            [contact.email],
            fail_silently=False,
        )
        
        messages.success(request, 'Reply sent successfully.')
        return redirect('contact_us_reply')

    contacts = ContactUs.objects.all()
    return render(request, 'contactus_reply.html', {'contacts': contacts})
