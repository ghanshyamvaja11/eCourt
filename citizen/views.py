from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseBadRequest
from users.models import *  # Import all models from users app
from cases.models import Case  # Assuming there is a Case model in the cases app
from notifications.models import Notification  # Assuming there is a Notification model in the notifications app

@login_required
def citizen_dashboard(request):
    return render(request, 'citizen_dashboard.html')

@login_required
def header(request):
    return render(request, 'citizen_header.html')

@login_required
def file_cases(request):
    if request.method == 'POST':
        # Handle case filing logic here
        case_title = request.POST.get('case_title')
        case_description = request.POST.get('case_description')
        case = Case.objects.create(
            title=case_title,
            description=case_description,
            filed_by=request.user.citizen
        )
        messages.success(request, 'Case filed successfully.')
        return redirect('my_cases')
    return render(request, 'file_cases.html')

@login_required
def my_cases(request):
    citizen = User.objects.get(user=request.user)
    cases = Case.objects.filter(filed_by=citizen)
    return render(request, 'my_cases.html', {'cases': cases})

@login_required
def efilling(request):
    return render(request, 'efilling.html')

@login_required
def notification(request):
    notifications = Notification.objects.filter(user=request.user)
    return render(request, 'notification.html', {'notifications': notifications})

@login_required
def citizen_profile(request):
    citizen = Citizen.objects.get(user=request.user)
    user = User.objects.get(id=citizen.user.id)
    return render(request, 'citizen_profile.html', {'citizen': citizen, 'user': user})

@login_required
def citizen_edit_profile(request):
    citizen = Citizen.objects.get(user=request.user)
    user = User.objects.get(id=citizen.user.id)
    if request.method == 'POST':
        name = request.POST.get('name', citizen.user.full_name)
        email = request.POST.get('email', user.email)
        phone = request.POST.get('phone', citizen.user.contact_number)
        national_id_type = request.POST.get('national_id_type', citizen.national_id_type)
        national_id = request.POST.get('national_id', citizen.national_id)
        
        # Add validations
        if not name:
            messages.error(request, 'Name is required')
            return redirect('citizen_profile')
        if not email:
            messages.error(request, 'Email is required')
            return redirect('citizen_profile')
        if not phone:
            messages.error(request, 'Phone number is required')
            return redirect('citizen_profile')
        if not national_id_type:
            messages.error(request, 'National ID type is required')
            return redirect('citizen_profile')
        if not national_id:
            messages.error(request, 'National ID is required')
            return redirect('citizen_profile')
        
        user.full_name = name
        user.email = email
        user.contact_number = phone
        citizen.national_id_type = national_id_type
        citizen.national_id = national_id
        
        # Add other fields as necessary
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        
        citizen.save()
        user.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('citizen_profile')
    else:
        return HttpResponseBadRequest("Invalid request method")
