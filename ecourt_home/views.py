from users.models import *
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from users.models import *


def index(request):
    return render(request, 'index.html')


def aboutus(request):
    return render(request, 'about_us.html')


def contactus(request):
    return render(request, 'contact_us.html')


def terms_and_conditions(request):
    return render(request, 'terms_and_conditions.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')


def signup(request):
    # if request.method == 'POST':
    #     # Extracting form data
    #     username = request.POST.get('username')
    #     full_name = request.POST.get('full_name')
    #     email = request.POST.get('email')
    #     contact_number = request.POST.get('contact_number')
    #     password = request.POST.get('password')
    #     address = request.POST.get('address')
    #     # Role: Admin, Lawyer, Judge, Citizen
    #     role = request.POST.get('register_as')
    #     cred1 = request.POST.get('cred1')  # License Number or National ID
    #     # Law Firm, National ID Type, or Court
    #     cred2 = request.POST.get('cred2')

    #     # Debug: Print submitted form data
    #     print(username, full_name, email, contact_number,
    #           password, address, role, cred1, cred2)

    #     # Validation: Check required fields
    #     if not all([username, full_name, email, password, address, role]):
    #         messages.error(request, "All required fields must be filled.")
    #         return redirect('signup')

    #     # Ensure unique username and email
    #     if User.objects.filter(username=username).exists():
    #         messages.error(request, "Username is already taken.")
    #         return redirect('signup')
    #     if User.objects.filter(email=email).exists():
    #         messages.error(request, "Email is already registered.")
    #         return redirect('signup')

    #     # Create the base User instance
    #     user = User(
    #         username=username,
    #         full_name=full_name,
    #         email=email.lower(),
    #         contact_number=contact_number,
    #         password=make_password(password),  # Hash the password
    #         address=address,
    #         user_type=role.upper()
    #     )

    #     try:
    #         user.save()  # Save the base user instance
    #     except Exception as e:    
    #         messages.error(request, f"Failed to create user account: {e}")
    #         return redirect('signup')

    # Render signup form
    return render(request, 'signup.html')

def login_view(request):
    # if request.method == "POST":
    #     user_type = request.POST.get('user_type')
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')

    #     # Authenticate the user
    #     user = authenticate(request, username=username, password=password)

    #     if user is not None:
    #         # Check if the user has the correct role
    #         if user.user_type == user_type:
    #             login(request, user)
    #             # Redirect to the appropriate dashboard based on user type
    #             if user.user_type == 'CITIZEN':
    #                 # Replace with actual URL name
    #                 return redirect('citizen_dashboard')
    #             elif user.user_type == 'LAWYER':
    #                 return redirect('lawyer_dashboard')
    #             elif user.user_type == 'JUDGE':
    #                 return redirect('judge_dashboard')
    #             else:
    #                 return redirect('admin_dashboard')  # For Admin role
    #         else:
    #             messages.error(
    #                 request, "User type does not match your credentials.")
    #     else:
    #         messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')