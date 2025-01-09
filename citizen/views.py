from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseBadRequest, JsonResponse
from django.contrib.auth import logout
from users.models import *  # Import all models from users app
from cases.models import Case, Judge, Document  # Ensure Document model is imported
from notifications.models import Notification  # Assuming there is a Notification model in the notifications app
import random
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings

@login_required(login_url='/login/')
def citizen_dashboard(request):
    return render(request, 'citizen_dashboard.html')

@login_required(login_url='/login/')
def header(request):
    return render(request, 'citizen_header.html')

@login_required(login_url='/login/')
def file_cases(request):
    Defendents = Citizen.objects.exclude(user=request.user)
    Users = User.objects.filter(user_type='LAWYER', is_active=0)
    Lawyers = Lawyer.objects.filter(user__in=Users)

    if request.method == 'POST':
        case_title = request.POST.get('case_title')
        case_type = request.POST.get('case_type')
        case_description = request.POST.get('case_description')
        defendant_name = request.POST.get('defendant')
        assigned_lawyer_name = request.POST.get('assigned_lawyer')
        case_documents = request.FILES.getlist('case_documents')

        try:
            defendant = User.objects.get(full_name=defendant_name).citizen
        except User.DoesNotExist:
            messages.error(request, 'Defendant not found.')
            return redirect('file_cases')

        assigned_lawyer = None
        if assigned_lawyer_name:
            try:
                assigned_lawyer = User.objects.get(full_name=assigned_lawyer_name).lawyer
            except User.DoesNotExist:
                messages.error(request, 'Assigned lawyer not found.')
                return redirect('file_cases')

        case_number = f"{case_type.upper()}-{random.randint(1000, 9999)}"
        # assigned_judge = random.choice(Judge.objects.all())

        case = Case.objects.create(
            case_number=case_number,
            plaintiff=request.user.citizen,
            defendant=defendant,
            assigned_lawyer=assigned_lawyer,
            # assigned_judge=assigned_judge,
            case_title=case_title,
            case_type=case_type,
            case_description=case_description,
            status='PENDING'
        )

        citizen = Citizen.objects.get(user=request.user)

        for document in case_documents:
            Document.objects.create(
                case=case,
                document_type='Case Document',
                file=document,
                uploaded_by=citizen
            )

        # # Send email to defendant
        # send_mail(
        #     'New Case Filed Against You',
        #     f'A new case titled "{case_title}" has been filed against you. Please log in to your account for more details.',
        #     settings.DEFAULT_FROM_EMAIL,
        #     [defendant.user.email],
        #     fail_silently=False,
        # )

        messages.success(request, 'Case filed successfully.')
        return redirect('my_cases')
    return render(request, 'file_case.html', {'Defendents': Defendents, 'Lawyers': Lawyers})

@login_required(login_url='/login/')
def my_cases(request):
    citizen = Citizen.objects.get(user=request.user)
    cases = Case.objects.filter(plaintiff=citizen)

    if request.method == 'POST':
        action = request.POST.get('action')
        case_id = request.POST.get('case_id')

        if action == 'upload_document':
            document_type = request.POST.get('document_type')
            file = request.FILES.get('file')
            case = Case.objects.get(id=case_id)
            print(document_type, file, case)

            Document.objects.create(
                case=case,
                document_type=document_type,
                file=file,
                uploaded_by=citizen
            )

            messages.success(request, 'Document uploaded successfully.')
            return redirect('my_cases')

    return render(request, 'my_cases.html', {'cases': cases})

@login_required(login_url='/login/')
def efilling(request):
    return render(request, 'efilling.html')

@login_required(login_url='/login/')
def notification(request):
    notifications = Notification.objects.filter(user=request.user)
    return render(request, 'notification.html', {'notifications': notifications})

@login_required(login_url='/login/')
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})

@login_required(login_url='/login/')
def edit_profile(request):
    user = request.user
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
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

@login_required(login_url='/login/')
def case_documents(request):
    case_id = request.GET.get('case_id')
    if not case_id:
        return HttpResponseBadRequest("Case ID is required")

    try:
        case = Case.objects.get(id=case_id)
        request.session['case_number'] = case.case_number
    except Case.DoesNotExist:
        return HttpResponseBadRequest("Invalid Case ID")

    documents = Document.objects.filter(case=case)
    return render(request, 'case_docs.html', {'documents': documents})

@login_required(login_url='/login/')
def notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-date_sent')
    return render(request, 'notifications.html', {'notifications': notifications})

@login_required(login_url='/login/')
def against_cases(request):
    citizen = Citizen.objects.get(user=request.user)
    cases = Case.objects.filter(defendant=citizen)

    if request.method == 'POST':
        action = request.POST.get('action')
        case_id = request.POST.get('case_id')

        if action == 'select_lawyer':
            assigned_lawyer_name = request.POST.get('assigned_lawyer')
            try:
                assigned_lawyer = User.objects.get(full_name=assigned_lawyer_name).lawyer
                case = Case.objects.get(id=case_id)
                case.assigned_lawyer = assigned_lawyer
                case.lawyer_accepted = False
                case.save()
                messages.success(request, 'Lawyer assigned successfully.')
            except User.DoesNotExist:
                messages.error(request, 'Assigned lawyer not found.')
            return redirect('against_cases')

    Users = User.objects.filter(user_type='LAWYER', is_active=0)
    Lawyers = Lawyer.objects.filter(user__in=Users)
    return render(request, 'against_cases.html', {'cases': cases, 'Lawyers': Lawyers})
