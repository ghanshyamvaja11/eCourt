from django.shortcuts import render, redirect, get_object_or_404
from users.models import *
from cases.models import *
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def admin_dashboard(request):
    # Fetch some data to display on the dashboard
    total_users = User.objects.count()
    total_cases = Case.objects.count()
    return render(request, 'admin_dashboard.html', {
        'total_users': total_users,
        'total_cases': total_cases,
    })

def header(request):
    return render(request, 'admin_header.html')

@login_required
def user_management(request):
    users = User.objects.all()
    return render(request, 'user_management.html', {'users': users})

@login_required
def citizens_management(request):
    citizens = User.objects.filter(user_type='CITIZEN')
    return render(request, 'citizens_management.html', {'citizens': citizens})

@login_required
def lawyers_management(request):
    lawyers = Lawyer.objects.all()
    return render(request, 'lawyers_management.html', {'lawyers': lawyers})

@login_required
def judges_management(request):
    judges = Judge.objects.all()
    return render(request, 'judges_management.html', {'judges': judges})

@login_required
def case_management(request):
    cases = Case.objects.all()
    return render(request, 'case_management.html', {'cases': cases})

@login_required
def case_status(request):
    cases = Case.objects.all()
    return render(request, 'case_status.html', {'cases': cases})

@login_required
def all_cases(request):
    cases = Case.objects.all()
    return render(request, 'all_cases.html', {'cases': cases})

# Example view for Pending Cases
@login_required
def pending_cases(request):
    cases = Case.objects.filter(status='PENDING')
    return render(request, 'pending_cases.html', {'cases': cases})

# Example view for Active Cases
@login_required
def active_cases(request):
    cases = Case.objects.filter(status='ACTIVE')
    return render(request, 'active_cases.html', {'cases': cases})

# Example view for Closed Cases
@login_required
def closed_cases(request):
    cases = Case.objects.filter(status='CLOSED')
    return render(request, 'closed_cases.html', {'cases': cases})

# Example view for Dismissed Cases
@login_required
def dismissed_cases(request):
    cases = Case.objects.filter(status='DISMISSED')
    return render(request, 'dismissed_cases.html', {'cases': cases})

@login_required
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

@login_required
def lawyer_approve_reject(request):
    lawyers = Lawyer.objects.filter(user__user_type='PENDING_LAWYER')
    return render(request, 'lawyer_request.html', {'lawyers': lawyers})

@login_required
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
            lawyer.user.save()
            messages.success(request, f"Lawyer {user.username} has been approved.")
        elif action == 'reject':
            lawyer.delete()
            user.delete()
            messages.success(request, f"Lawyer {user.username} has been rejected.")
        else:
            messages.error(request, "Invalid action.")
        return redirect('admin_dashboard')

    return render(request, 'approve_reject_lawyer.html', {'lawyer': lawyer})

@login_required
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        user.username = request.POST['username']
        user.full_name = request.POST['full_name']
        user.email = request.POST['email']
        user.contact_number = request.POST['contact_number']
        user.address = request.POST['address']
        if 'profile_image' in request.FILES:
            user.profile_image = request.FILES['profile_image']
        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')
    return render(request, 'edit_profile.html', {'user': user})
