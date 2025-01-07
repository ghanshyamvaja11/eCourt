from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseBadRequest
from users.models import *  # Import all models from users app
from cases.models import Case  # Assuming there is a Case model in the cases app
from django.contrib.auth import logout

@login_required(login_url='/login/')
def judge_dashboard(request):
    return render(request, 'judge_dashboard.html')

@login_required(login_url='/login/')
def judge_assigned_cases(request):
    judge = Judge.objects.get(user=request.user)
    cases = Case.objects.filter(assigned_to=judge)
    return render(request, 'judge_assigned_cases.html', {'cases': cases})

@login_required(login_url='/login/')
def judge_hearing(request):
    judge = Judge.objects.get(user=request.user)
    hearings = Case.objects.filter(assigned_to=judge, status='Scheduled')
    return render(request, 'judge_hearing.html', {'hearings': hearings})

@login_required(login_url='/login/')
def outcome(request):
    judge = Judge.objects.get(user=request.user)
    outcomes = Case.objects.filter(assigned_to=judge, status__in=['Verdict Delivered', 'Adjourned'])
    return render(request, 'outcome.html', {'outcomes': outcomes})

@login_required(login_url='/login/')
def case_doc(request):
    judge = Judge.objects.get(user=request.user)
    cases = Case.objects.filter(assigned_to=judge)
    return render(request, 'case_doc.html', {'cases': cases})

@login_required(login_url='/login/')
def judge_profile(request):
    judge = Judge.objects.get(user=request.user)
    user = User.objects.get(id=judge.user.id)
    return render(request, 'judge_profile.html', {'judge': judge, 'user': user})

@login_required(login_url='/login/')
def judge_edit_profile(request):
    judge = Judge.objects.get(user=request.user)
    user = User.objects.get(id=judge.user.id)
    if request.method == 'POST':
        name = request.POST.get('name', judge.user.full_name)
        email = request.POST.get('email', user.email)
        phone = request.POST.get('phone', judge.user.contact_number)
        court = request.POST.get('court', judge.court)
        
        # Add validations
        if not name:
            messages.error(request, 'Name is required')
            return redirect('judge_profile')
        if not email:
            messages.error(request, 'Email is required')
            return redirect('judge_profile')
        if not phone:
            messages.error(request, 'Phone number is required')
            return redirect('judge_profile')
        if not court:
            messages.error(request, 'Court is required')
            return redirect('judge_profile')
        
        user.full_name = name
        user.email = email
        user.contact_number = phone
        judge.court = court
        
        # Add other fields as necessary
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        
        judge.save()
        user.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('judge_profile')
    else:
        return HttpResponseBadRequest("Invalid request method")

@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout
