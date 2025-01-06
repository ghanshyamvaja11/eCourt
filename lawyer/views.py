from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseBadRequest
from users.models import *  # Import all models from users app
from cases.models import Case  # Assuming there is a Case model in the cases app

@login_required
def lawyer_dashboard(request):
    return render(request, 'lawyer_dashboard.html')

def header(request):
    return render(request,'lawyer_header.html')

@login_required
def assigned_cases(request):
    lawyer = Lawyer.objects.get(user=request.user)
    cases = Case.objects.filter(assigned_to=lawyer)
    return render(request, 'assigned_cases.html', {'cases': cases})

@login_required
def hearings(request):
    # Logic for hearings
    return render(request, 'hearings.html')

@login_required
def efilling(request):
    return render(request, 'efilling.html')

@login_required
def lawyer_profile(request):
    lawyer = Lawyer.objects.get(user=request.user)
    user = User.objects.get(id=lawyer.user.id)
    return render(request, 'lawyer_profile.html', {'lawyer': lawyer, 'user': user})

@login_required
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
