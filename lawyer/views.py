from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponse
from django.contrib.auth import logout
from django.core.mail import send_mail
from users.models import *  # Import all models from users app
from cases.models import *  # Assuming there is a Case model in the cases app
from notifications.models import Notification

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
    cases = Case.objects.filter(assigned_lawyer=lawyer)
    return render(request, 'assigned_cases.html', {'cases': cases})

@login_required(login_url='/login/')
def hearings(request):
    # Clear all previous messages
    storage = messages.get_messages(request)
    storage.used = True

    hearings = Hearing.objects.all()
    return render(request, 'hearings.html', {'hearings': hearings})

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
def profile(request):
    # Clear all previous messages
    storage = messages.get_messages(request)
    storage.used = True

    user = request.user
    return render(request, 'profile.html', {'user': user})

@login_required(login_url='/login/')
def edit_profile(request):
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
        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')
    return render(request, 'edit_profile.html', {'user': user})

@login_required(login_url='/login/')
def logout_view(request):
    # Clear all previous messages
    storage = messages.get_messages(request)
    storage.used = True

    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

@login_required(login_url='/login/')
def case_requests(request):
    # Clear all previous messages
    storage = messages.get_messages(request)
    storage.used = True

    lawyer = Lawyer.objects.get(user=request.user)
    cases = Case.objects.filter(assigned_lawyer=lawyer, lawyer_accepted=False)
    return render(request, 'case_requests.html', {'cases': cases})

@login_required(login_url='/login/')
def accept_case(request):
    # Clear all previous messages
    storage = messages.get_messages(request)
    storage.used = True

    case_id = request.GET.get('case_id')
    case = Case.objects.get(id=case_id)
    case.lawyer_accepted = True
    assigned_judge = random.choice(Judge.objects.all())
    case.assigned_judge = assigned_judge
    case.save()

    send_mail(
        'Case Accepted',
        f'Your case {case.case_number} has been accepted by the lawyer.',
        'ecourtofficially@gmail.com',
        [case.plaintiff.user.email],
        fail_silently=False,
    )
    messages.success(request, 'Case accepted successfully.')
    return redirect('case_requests')

@login_required(login_url='/login/')
def decline_case(request):
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

    case.assigned_lawyer = None
    case.save()

    messages.success(request, 'Case declined successfully.')
    return redirect('case_requests')

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
