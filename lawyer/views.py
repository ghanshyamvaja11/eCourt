from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.contrib.auth import logout
from django.core.mail import send_mail
from users.models import *  # Import all models from users app
from cases.models import Case, Document  # Assuming there is a Case model in the cases app
from notifications.models import Notification

@login_required(login_url='/login/')
def lawyer_dashboard(request):
    return render(request, 'lawyer_dashboard.html')

def header(request):
    return render(request,'lawyer_header.html')

@login_required(login_url='/login/')
def assigned_cases(request):
    lawyer = Lawyer.objects.get(user=request.user)
    cases = Case.objects.filter(assigned_to=lawyer)
    return render(request, 'assigned_cases.html', {'cases': cases})

@login_required(login_url='/login/')
def hearings(request):
    # Logic for hearings
    return render(request, 'hearings.html')

@login_required(login_url='/login/')
def efilling(request):
    return render(request, 'efilling.html')

@login_required(login_url='/login/')
def lawyer_profile(request):
    lawyer = Lawyer.objects.get(user=request.user)
    user = User.objects.get(id=lawyer.user.id)
    return render(request, 'lawyer_profile.html', {'lawyer': lawyer, 'user': user})

@login_required(login_url='/login/')
def lawyer_edit_profile(request):
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
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

@login_required(login_url='/login/')
def case_requests(request):
    lawyer = Lawyer.objects.get(user=request.user)
    cases = Case.objects.filter(assigned_lawyer=lawyer, lawyer_accepted=False)
    return render(request, 'case_requests.html', {'cases': cases})

@login_required(login_url='/login/')
def accept_case(request):
    case_id = request.GET.get('case_id')
    case = Case.objects.get(id=case_id)
    case.lawyer_accepted = True
    case.save()

    send_mail(
        'Case Accepted',
        f'Your case {case.case_number} has been accepted by the lawyer.',
        'ecourtofficially@gmail.com',
        [case.plaintiff.user.email],
        fail_silently=False,
    )

    send_mail(
        'Case Accepted',
        f'Your case {case.case_number} has been accepted by the lawyer.',
        'ecourtofficially@gmail.com',
        [case.defendant.user.email],
        fail_silently=False,
    )

    messages.success(request, 'Case accepted successfully.')
    return redirect('case_requests')

@login_required(login_url='/login/')
def decline_case(request):
    case_id = request.GET.get('case_id')
    case = Case.objects.get(id=case_id)

    send_mail(
        'Case Declined',
        f'Your case {case.case_number} has been declined by the lawyer.',
        'ecourtofficially@gmail.com',
        [case.plaintiff.user.email],
        fail_silently=False,
    )

    case.assigned_lawyer = None
    case.save()

    messages.success(request, 'Case declined successfully.')
    return redirect('case_requests')

@login_required(login_url='/login/')
def notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-date_sent')
    return render(request, 'notifications.html', {'notifications': notifications})

@login_required(login_url='/login/')
def client_case_documents(request):
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