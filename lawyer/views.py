from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponse
from django.contrib.auth import logout
from django.core.mail import send_mail
import random
from users.models import *  # Import all models from users app
from users.models import Judge
from cases.models import *  # Assuming there is a Case model in the cases app
from notifications.models import Notification
from administrator.models import * # Assuming there is
from django.db.models import Q
@login_required(login_url='/login/')
def lawyer_dashboard(request):
    return render(request, 'lawyer_dashboard.html')

def header(request):
    return render(request,'lawyer_header.html')

@login_required(login_url='/login/')
def assigned_cases(request):
    # Clear all previous messages
    storage = messages.get_messages(request)
    storage.used = True

    lawyer = Lawyer.objects.get(user=request.user)
    plaintiff_cases = Case.objects.filter(assigned_lawyer=lawyer, lawyer_accepted=True)
    defendant_cases = Case.objects.filter(
        defendant_lawyer=lawyer, defendant_lawyer_accepted=True)
    cases = plaintiff_cases | defendant_cases
    cases = cases.distinct()
    return render(request, 'assigned_cases.html', {'cases': cases})

@login_required(login_url='/login/')
def hearings(request):
    # Clear all previous messages
    storage = messages.get_messages(request)
    storage.used = True

    hearings = Hearing.objects.all()
    return render(request, 'lawyer_hearings.html', {'hearings': hearings})

@login_required(login_url='/login/')
def efilling(request):
    # Clear all previous messages
    storage = messages.get_messages(request)
    storage.used = True

    lawyer = Lawyer.objects.get(user=request.user)
    cases = Case.objects.filter(assigned_lawyer=lawyer)

    if request.method == 'POST':
        action = request.POST.get('action')
        case_id = request.POST.get('case_id')

        if action == 'upload_document':
            document_type = request.POST.get('document_type')
            file = request.FILES.get('file')
            case = Case.objects.get(id=case_id)

            Document.objects.create(
                case=case,
                document_type=document_type,
                file=file,
                uploaded_by=lawyer
            )

            messages.success(request, 'Document uploaded successfully.')
            return redirect('efilling')

    return render(request, 'efilling.html', {'cases': cases})

@login_required(login_url='/login/')
def lawyer_profile(request):
    # Clear all previous messages
    storage = messages.get_messages(request)
    storage.used = True

    lawyer = Lawyer.objects.get(user=request.user)
    user = User.objects.get(id=lawyer.user.id)
    return render(request, 'lawyer_profile.html', {'lawyer': lawyer, 'user': user})

@login_required(login_url='/login/')
def lawyer_edit_profile(request):
    # Clear all previous messages
    storage = messages.get_messages(request)
    storage.used = True

    lawyer = Lawyer.objects.get(user=request.user)
    user = User.objects.get(id=lawyer.user.id)
    if request.method == 'POST':
        name = request.POST.get('name', lawyer.user.full_name)
        email = request.POST.get('email', user.email)
        phone = request.POST.get('phone', lawyer.user.contact_number)
        license_number = request.POST.get('license_number', lawyer.license_number)
        law_firm = request.POST.get('law_firm', lawyer.law_firm)
        
        # Add validations
        if not name:
            messages.error(request, 'Name is required')
            return redirect('lawyer_profile')
        if not email:
            messages.error(request, 'Email is required')
            return redirect('lawyer_profile')
        if not phone:
            messages.error(request, 'Phone number is required')
            return redirect('lawyer_profile')
        if not license_number:
            messages.error(request, 'License number is required')
            return redirect('lawyer_profile')
        
        user.full_name = name
        user.email = email
        user.contact_number = phone
        lawyer.license_number = license_number
        lawyer.law_firm = law_firm
        
        # Add other fields as necessary
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        
        lawyer.save()
        user.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('lawyer_profile')
    else:
        return HttpResponseBadRequest("Invalid request method")

@login_required(login_url='/login/')
def lawyer_profile(request):
    # Clear all previous messages
    storage = messages.get_messages(request)
    storage.used = True

    user = request.user
    lawyer = Lawyer.objects.get(user=user)
    return render(request, 'lawyer_profile.html', {'user': user, 'lawyer': lawyer})

@login_required(login_url='/login/')
def lawyer_edit_profile(request):
    # Clear all previous messages
    storage = messages.get_messages(request)
    storage.used = True

    user = request.user
    if request.method == 'POST':
        user.username = user.username
        user.full_name = request.POST['full_name']
        user.email = request.POST['email']
        user.contact_number = request.POST['contact_number']
        user.address = request.POST['address']
        if request.FILES.get('profile_image'):
            user.profile_picture = request.FILES['profile_image']

        # Add validations
        if not user.full_name:
            messages.error(request, 'Name is required')
            return redirect('lawyer_profile')
        if not user.email:
            messages.error(request, 'Email is required')
            return redirect('lawyer_profile')
        if not user.contact_number:
            messages.error(request, 'Phone number is required')
            return redirect('lawyer_profile')
        if not user.address:
            messages.error(request, 'addrress is required')
            return redirect('lawyer_profile')

        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('lawyer_profile')
    return render(request, 'lawyer_edit_profile.html', {'user': user})

@login_required(login_url='/login/')
def logout_view(request):
    # Clear all previous messages
    storage = messages.get_messages(request)
    storage.used = True

    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

@login_required(login_url='/login/')
def plaintiff_case_requests(request):
    # Clear all previous messages
    storage = messages.get_messages(request)
    storage.used = True

    lawyer = Lawyer.objects.get(user=request.user)
    plantiff_cases = Case.objects.filter(assigned_lawyer=lawyer, lawyer_accepted=False)

    cases = plantiff_cases

    return render(request, 'plaintiff_case_requests.html', {'cases': cases})

@login_required(login_url='/login/')
def plaintiff_accept_case(request):
    # Clear all previous messages
    storage = messages.get_messages(request)
    storage.used = True

    case_id = request.GET.get('case_id')
    case = Case.objects.get(id=case_id)
    case.lawyer_accepted = True
    assigned_judge = random.choice(Judge.objects.all())
    case.assigned_judge = assigned_judge
    judge_instance = Judge.objects.get(user=assigned_judge.user)
    judge_instance.cases_assigned += 1
   
    judge_instance.save()
    case.status = 'ACTIVE'
    case.save()

    send_mail(
        'Case Accepted',
        f'Your case {case.case_number} has been accepted by the lawyer.',
        'ecourtofficially@gmail.com',
        [case.plaintiff.user.email],
        fail_silently=False,
    )
    messages.success(request, 'Case accepted successfully.')
    return redirect('plaintiff_case_requests')

@login_required(login_url='/login/')
def plaintiff_decline_case(request):
    # Clear all previous messages
    storage = messages.get_messages(request)
    storage.used = True

    case_id = request.GET.get('case_id')
    case = Case.objects.get(id=case_id)

    send_mail(
        'Case Declined',
        f'Your case {case.case_number} has been declined by the lawyer.',
        'ecourtofficially@gmail.com',
        [case.plaintiff.user.email],
        fail_silently=False,
    )

    if case.assigned_lawyer:
        case.assigned_lawyer = None
    
    if case.defendant_lawyer:
        case.defendant_lawyer = None
    case.save()

    messages.success(request, 'Case declined successfully.')
    return redirect('plaintiff_case_requests')


@login_required(login_url='/login/')
def defendant_case_requests(request):
    # Clear all previous messages
    storage = messages.get_messages(request)
    storage.used = True

    lawyer = Lawyer.objects.get(user=request.user)
    
    defendant_cases = Case.objects.filter(
        defendant_lawyer=lawyer, defendant_lawyer_accepted=False)
    cases = defendant_cases

    return render(request, 'defendant_case_requests.html', {'cases': cases})


@login_required(login_url='/login/')
def defendant_accept_case(request):
    # Clear all previous messages
    storage = messages.get_messages(request)
    storage.used = True

    case_id = request.GET.get('case_id')
    case = Case.objects.get(id=case_id)
    case.defendant_lawyer_accepted = True
    case.status = 'ACTIVE'
    case.save()

    send_mail(
        'Case Accepted',
        f'Your case {case.case_number} has been accepted by the lawyer.',
        'ecourtofficially@gmail.com',
        [case.defendant.user.email],
        fail_silently=False,
    )
    messages.success(request, 'Case accepted successfully.')
    return redirect('defendant_case_requests')


@login_required(login_url='/login/')
def defendant_decline_case(request):
    # Clear all previous messages
    storage = messages.get_messages(request)
    storage.used = True

    case_id = request.GET.get('case_id')
    case = Case.objects.get(id=case_id)

    send_mail(
        'Case Declined',
        f'Your case {case.case_number} has been declined by the lawyer.',
        'ecourtofficially@gmail.com',
        [case.defendant.user.email],
        fail_silently=False,
    )

    if case.defendant_lawyer:
        case.defendant_lawyer = None
    case.save()

    messages.success(request, 'Case declined successfully.')
    return redirect('defendant_case_requests')

@login_required(login_url='/login/')
def notifications(request):
    # Clear all previous messages
    storage = messages.get_messages(request)
    storage.used = True

    notifications = Notification.objects.filter(user=request.user).order_by('-date_sent')
    return render(request, 'notifications.html', {'notifications': notifications})

@login_required(login_url='/login/')
def client_case_documents(request):
    # Clear all previous messages
    storage = messages.get_messages(request)
    storage.used = True

    case_id = request.GET.get('case_id')
    if not case_id:
        return HttpResponseBadRequest("Case ID is required")

    try:
        case = Case.objects.get(id=case_id)
        request.session['case_number'] = case.case_number
    except Case.DoesNotExist:
        return HttpResponseBadRequest("Invalid Case ID")

    documents = Document.objects.filter(case=case)
    return render(request, 'client_case_docs.html', {'documents': documents})

@login_required(login_url='/login/')
def logout_view(request):
    # Clear all previous messages
    storage = messages.get_messages(request)
    storage.used = True

    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

def request_payment(request, case_id):
    # Fetch the lawyer object for the current user
    try:
        lawyer = Lawyer.objects.get(user=request.user)
    except Lawyer.DoesNotExist:
        lawyer = None  # Handle the absence of a lawyer

    if lawyer:
        # Try to fetch the cases where the lawyer is involved
        try:
            plaintiff_case = Case.objects.get(id=case_id, assigned_lawyer=lawyer)
        except Case.DoesNotExist:
            plaintiff_case = None  # Handle the absence of a plaintiff case

        try:
            defendant_case = Case.objects.get(id=case_id, defendant_lawyer=lawyer)
        except Case.DoesNotExist:
            defendant_case = None  # Handle the absence of a defendant case

        # Combine the cases if they exist
        if plaintiff_case and defendant_case:
            cases = plaintiff_case | defendant_case  # Combine the cases
        elif plaintiff_case:
            cases = plaintiff_case
        elif defendant_case:
            cases = defendant_case
        else:
            cases = 'no cases avaiable'  # No cases found

    else:
        cases = 'no lawyers avaiable'  # No lawyer found

    if plaintiff_case:
        if request.method == 'POST':
            amount = request.POST['amount']
            description = request.POST['description']
            Payment.objects.create(case=plaintiff_case, amount=amount, description=description)
            Notification.objects.create(
                user=plaintiff_case.plaintiff.user,
                message=f'You have a new payment request for case {plaintiff_case.case_number}.'
            )
            # Send email to client
            send_mail(
                'Payment Request',
                f'You have a new payment request for case {plaintiff_case.case_number}.',
                'ecourtofficially@gmail.com',
                [plaintiff_case.plaintiff.user.email],
                fail_silently=False,
            )
    else:
        if defendant_case:
            if request.method == 'POST':
                amount = request.POST['amount']
                description = request.POST['description']
                Payment.objects.create(case=defendant_case, amount=amount, description=description)

                Notification.objects.create(
                user=defendant_case.defendant.user,
                message=f'You have a new payment request for case {defendant_case.case_number}.'
            )
                
                # Send email to client
            send_mail(
                'Payment Request',
                f'You have a new payment request for case {defendant_case.case_number}.',
                'ecourtofficially@gmail.com',
                [plaintiff_case.defendant.user.email],
                fail_silently=False,
            )
        return redirect('lawyer_dashboard')
    return render(request, 'request_payment.html', {'case': cases})
