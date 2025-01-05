from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from users.models import *
from django.contrib import messages
from django.http import HttpResponse

# Create your views here.
def dashbord(request):
    return render(request,'admin_dashbord.html')
def header(request):
    return render(request,'admin_header.html')
def user_management(request):
    return render(request,'user_management.html')
   
def citizens_management(request):
    return render(request,' citizens_management.html')
def lawyers_management(request):
    return render(request,'lawyers_management.html')
def judges_management(request):
    return render(request,'judges_management.html')
def case_management(request):
    return render(request,'case_management.html')
def case_status(request):
    return render(request,'case_status.html')
def all_cases(request):
    return render(request,'all_cases.html')
# Example view for Pending Cases
def pending_cases(request):
    # Your logic for fetching pending cases
    return render(request, 'pending_cases.html')

# Example view for Active Cases
def active_cases(request):
    # Your logic for fetching active cases
    return render(request, 'active_cases.html')

# Example view for Closed Cases
def closed_cases(request):
    # Your logic for fetching closed cases
    return render(request, 'closed_cases.html')

# Example view for Dismissed Cases
def dismissed_cases(request):
    # Your logic for fetching dismissed cases
    return render(request, 'dismissed_cases.html')
def add_judge(request):
    # Your logic for fetching dismissed cases
    return render(request, 'add_judge.html')

def lawyer_approve_reject(request):
    # Your logic for fetching dismissed cases
    return render(request, 'lawyer_request.html')


def approve_or_reject_lawyer(request, username):
    # Fetch the user by username
    user = get_object_or_404(User, username=username)

    # Check if the user is a Lawyer
    try:
        lawyer = Lawyer.objects.get(user=user)
    except Lawyer.DoesNotExist:
        messages.error(request, "This user is not a lawyer.")
        return redirect('admin_dashboard')  # Redirect to the admin dashboard

    # Handle the approve/reject action
    if request.method == "POST":
        action = request.POST.get('action')

        if action == 'approve':
            lawyer.user.user_type = 'LAWYER'  # Approve and change user type to LAWYER
            lawyer.user.save()
            messages.success(
                request, f"Lawyer {user.username} has been approved.")
        elif action == 'reject':
            lawyer.delete()  # Remove the lawyer record
            user.delete()  # Optionally remove the user as well
            messages.success(
                request, f"Lawyer {user.username} has been rejected.")
        else:
            messages.error(request, "Invalid action.")

        return redirect('admin_dashboard')  # Redirect back to admin dashboard

    return render(request, 'approve_reject_lawyer.html', {
        'lawyer': lawyer,
    })

def profile(request):
    # Your logic for fetching dismissed cases
    return render(request, 'profile.html')
def edit_profile(request):
    # Your logic for fetching dismissed cases
    return render(request, 'edit_profile.html')
    