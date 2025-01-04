from django.contrib.auth.models import User
from django.db import transaction
from users.models import *
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from users.models import *
from django.core.mail import send_mail

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
    if request.method == 'POST':
        # Extracting form data
        username = request.POST.get('username')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')
        password = request.POST.get('password')
        address = request.POST.get('address')
        # Role: Admin, Lawyer, Judge, Citizen
        role = request.POST.get('register_as')
        National_id_type = request.POST.get('National_id_type')  # License or National ID
        # Law Firm, Court Name, or National ID Type
        National_id_number = request.POST.get('National_id_number')
        License_number = request.POST.get('License_number')  # License or National ID
        # Law Firm, Court Name, or National ID Type
        Law_firm = request.POST.get('Law_firm')

        # Validation
        # Initialize a list to collect all error messages
        errors = []

        # General validations
        if not all([username, full_name, email, password, address, role]):
            errors.append("All fields are required.")

        if User.objects.filter(username=username).exists():
            errors.append("Username already exists.")
        if User.objects.filter(email=email).exists():
            errors.append("Email is already registered.")
        if User.objects.filter(contact_number=contact_number).exists():
            errors.append("Contact number is already registered.")

        # Role-specific validations
        if role == 'LAWYER':
            if not all([License_number, Law_firm]):
                errors.append(
                    "License number and law firm are required for lawyers.")
        elif role == 'JUDGE':
            if not National_id_type:
                errors.append("Court name is required for judges.")
        elif role == 'CITIZEN':
            if not National_id_type:
                errors.append("National ID is required for citizens.")
            if not National_id_number or National_id_number not in ['AADHAR', 'PASSPORT', 'VOTER ID CARD', 'DRIVING LICENSE']:
                errors.append(
                    "National ID type is required and must be Aadhar, Passport, Voter ID Card, or Driving License.")
            else:
                # National ID Type-Specific Validations
                if National_id_number == 'AADHAR':
                    if not National_id_type.isdigit() or len(National_id_type) != 12:
                        errors.append(
                            "Aadhar number must be a 12-digit numeric value.")
                elif National_id_number == 'PASSPORT':
                    if len(National_id_type) != 8 or not (National_id_type[0].isalpha() and National_id_type[1:].isdigit()):
                        errors.append(
                            "Passport number must be 8 characters, starting with a letter followed by 7 digits.")
                elif National_id_number == 'VOTER ID CARD':
                    if len(National_id_type) != 10 or not (National_id_type[:3].isalpha() and National_id_type[3:].isdigit()):
                        errors.append(
                            "Voter ID Card number must be 10 characters, starting with 3 letters followed by 7 digits.")
                elif National_id_number == 'DRIVING LICENSE':
                    if len(National_id_type) < 8 or len(National_id_type) > 16 or not any(char.isdigit() for char in National_id_type) or not any(char.isalpha() for char in National_id_type):
                        errors.append(
                            "Driving License number must be between 8-16 characters and contain both letters and numbers.")

        # If there are any errors, display them all and redirect to signup
        if errors:
            messages.error(request, " ".join(errors))
            return redirect('signup')

        # Create the User and specific subclass object
        try:
            with transaction.atomic():
                # Create base User
                if role != 'lawyer':
                    is_active = 1
                else:
                    is_active = 0
                    password = make_password(password)
                user = User.objects.create_user(
                    username=username,
                    full_name=full_name,
                    email=email.lower(),
                    contact_number=contact_number,
                    address=address,
                    user_type=role.upper(),
                    is_active = is_active
                )
                user.set_password(password)
                user.save()

                # Create role-specific instance
                if role.lower() == 'lawyer':
                    if not all([License_number, Law_firm]):
                        print(License_number, Law_firm)
                        messages.error(
                            request, "Both license number and law firm are required for Lawyer.")
                        return redirect('signup')
                    Lawyer.objects.create(
                        user=user,
                        license_number=License_number,
                        law_firm=Law_firm
                    )

                    # Send email to lawyer for account approval
                    send_mail(
                        'Account Registration Pending Approval',
                        f"Dear {full_name},\n\nThank you for registering on eCourt. Your account is currently pending approval. You will be able to log in once an administrator reviews and approves your account.\n\nBest regards,\neCourt Team",
                        'noreply@ecourt.com',  # Replace with your email
                        [email],
                        fail_silently=False,
                    )

                elif role.lower() == 'judge':
                    if not National_id_type:
                        messages.error(
                            request, "Court name is required for Judge.")
                        return redirect('signup')
                    Judge.objects.create(
                        user=user,
                        court=National_id_type
                    )

                elif role.lower() == 'citizen':
                    if not all([National_id_type, National_id_number]):
                        messages.error(
                            request, "National ID type and National ID are required for Citizen.")
                        return redirect('signup')
                    Citizen.objects.create(
                        user=user,
                        national_id_type=National_id_type,
                        national_id=National_id_number
                    )
                # Send registration success email for non-lawyers
            if role.lower() != 'lawyer':
                send_mail(
                    'Registration Successful',
                    f"Dear {full_name},\n\nWelcome to eCourt! Your account has been successfully created, and you can now log in to access your dashboard.\n\nBest regards,\neCourt Team",
                    'noreply@ecourt.com',  # Replace with your email
                    [email],
                    fail_silently=False,
                )

                messages.success(
                    request, f"{role.capitalize()} registered successfully!")
                return redirect('login')

        except Exception as e:
            messages.error(
                request, f"Failed to register {role.capitalize()}: {e}")
            return redirect('signup')

    return render(request, 'signup.html')


def login_view(request):
    if request.method == "POST":
        # Get form data
        user_type = request.POST.get('user_type')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Print form data to debug
        print(
            f"Username: {username}, Password: {password}, User Type: {user_type}")
        password 
        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        # Check if the user is authenticated
        if user is not None:
            # Print authenticated user info
            print(
                f"Authenticated User: {user.username}, User Type: {user.user_type}")

            # Check if the user type matches
            if user.user_type == user_type.upper():  # Ensure case-insensitive comparison
                # Log the user in
                login(request, user)
                request.session['username'] = username
                print(f"Logged in User: {username}")

                # Redirect based on user type
                if user.user_type == 'CITIZEN':
                    return redirect('citizen_dashboard')
                elif user.user_type == 'LAWYER':
                    return redirect('lawyer_dashboard')
                elif user.user_type == 'JUDGE':
                    return redirect('judge_dashboard')
                elif user.user_type == 'ADMIN':
                    return redirect('admin_dashboard')
                else:
                    messages.error(request, "Unknown user type.")
            else:
                messages.error(
                    request, "User type does not match your credentials.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')
