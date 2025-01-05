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
import random
from django.conf import settings

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
        role = request.POST.get('register_as')
        National_id_type = request.POST.get('National_id_type')
        National_id_number = request.POST.get('National_id_number')
        License_number = request.POST.get('License_number')
        Law_firm = request.POST.get('Law_firm')

        # Validation
        errors = []

        # General validations
        if not all([username, full_name, email, password, address, role]):
            errors.append("All fields are required.")

        if User.objects.filter(username=username).exists():
            errors.append("Username already exists.")
        if User.objects.filter(email=email).exists():
            errors.append("Email is already registered.")
        # Role-specific validations
        if role == 'LAWYER':
            if not all([License_number, Law_firm]):
                errors.append("License number and law firm are required for lawyers.")
        elif role == 'JUDGE':
            if not National_id_type:
                errors.append("Court name is required for judges.")
        elif role == 'CITIZEN':
            if not National_id_type or not National_id_number:
                errors.append("National ID type and number are required for citizens.")
            elif National_id_type not in ['AADHAR', 'PASSPORT', 'VOTER ID CARD', 'DRIVING LICENSE']:
                errors.append("National ID type must be Aadhar, Passport, Voter ID Card, or Driving License.")
            else:
                # National ID Type-Specific Validations
                if National_id_type == 'AADHAR':
                    if not National_id_number.isdigit() or len(National_id_number) != 12:
                        errors.append("Aadhar number must be a 12-digit numeric value.")
                elif National_id_type == 'PASSPORT':
                    if len(National_id_number) != 8 or not (National_id_number[0].isalpha() and National_id_number[1:].isdigit()):
                        errors.append("Passport number must be 8 characters, starting with a letter followed by 7 digits.")
                elif National_id_type == 'VOTER ID CARD':
                    if len(National_id_number) != 10 or not (National_id_number[:3].isalpha() and National_id_number[3:].isdigit()):
                        errors.append("Voter ID Card number must be 10 characters, starting with 3 letters followed by 7 digits.")
                elif National_id_type == 'DRIVING LICENSE':
                    if len(National_id_number) < 8 or len(National_id_number) > 16 or not any(char.isdigit() for char in National_id_number) or not any(char.isalpha() for char in National_id_number):
                        errors.append("Driving License number must be between 8-16 characters and contain both letters and numbers.")

        # If there are any errors, display them all and redirect to signup
        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('signup')

        # Create the User and specific subclass object
        try:
            with transaction.atomic():
                # Create base User
                if role != 'lawyer':
                    is_active = 1
                else:
                    is_active = 0
                user = User.objects.create_user(
                    username=username,
                    full_name=full_name,
                    email=email.lower(),
                    contact_number=contact_number,
                    address=address,
                    user_type=role.upper(),
                    is_active=is_active
                )
                user.set_password(password)
                user.save()

                # Create role-specific instance
                if role.lower() == 'lawyer':
                    Lawyer.objects.create(
                        user=user,
                        license_number=License_number,
                        law_firm=Law_firm
                    )
                    send_mail(
                        'Account Registration Pending Approval',
                        f"Dear {full_name},\n\nThank you for registering on eCourt. Your account is currently pending approval. You will be able to log in once an administrator reviews and approves your account.\n\nBest regards,\neCourt Team",
                        'noreply@ecourt.com',
                        [email],
                        fail_silently=False,
                    )
                elif role.lower() == 'judge':
                    Judge.objects.create(
                        user=user,
                        court=National_id_type
                    )
                elif role.lower() == 'citizen':
                    Citizen.objects.create(
                        user=user,
                        national_id_type=National_id_type,
                        national_id=National_id_number
                    )
                if role.lower() != 'lawyer':
                    send_mail(
                        'Registration Successful',
                        f"Dear {full_name},\n\nWelcome to eCourt! Your account has been successfully created, and you can now log in to access your dashboard.\n\nBest regards,\neCourt Team",
                        'noreply@ecourt.com',
                        [email],
                        fail_silently=False,
                    )
                messages.success(request, f"{role.capitalize()} registered successfully!")
                return redirect('login')

        except Exception as e:
            messages.error(request, f"Failed to register {role.capitalize()}: {e}")
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

def faq(request):
    return render(request,'faq.html')

    
def login_with_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        request.session['temp_email'] = email
        user = User.objects.filter(email=email).first()
        if user:
            otp = random.randint(100000, 999999)
            request.session['otp'] = otp
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp}. Please use this code to log in to your account.',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            messages.success(request, 'OTP has been sent to your email.')
            return redirect('verify_login_otp')
        else:
            messages.error(request, 'User not found.')
            return render(request, 'login_with_otp.html')
    return render(request, 'login_with_otp.html')

def verify_login_otp(request):
    if request.method == 'POST':
        email = request.session.get('temp_email')
        otp = request.POST.get('otp')
        user = User.objects.filter(email=email).first()
        if user and str(request.session.get('otp')) == otp:
            login(request, user)
            del request.session['otp']
            messages.success(request, 'Logged in successfully.')
            return redirect('index')
        else:
            messages.error(request, 'Invalid OTP.')
            return render(request, 'verify_login_otp.html')
    return render(request, 'verify_login_otp.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        request.session['temp_email'] = email
        user = User.objects.filter(email=email).first()
        if user:
            otp = random.randint(100000, 999999)
            request.session['otp'] = otp
            send_mail(
                'Your Password Reset OTP Code',
                f'Your OTP code is {otp}. Please use this code to reset your password.',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            messages.success(request, 'OTP has been sent to your email.')
            return redirect('verify_forgot_password_otp')
        else:
            messages.error(request, 'User not found.')
            return render(request, 'forgot_password.html')
    return render(request, 'forgot_password.html')

def verify_forgot_password_otp(request):
    if request.method == 'POST':
        email = request.session.get('temp_email')
        otp = request.POST.get('otp')
        user = User.objects.filter(email=email).first()
        if user and str(request.session.get('otp')) == otp:
            del request.session['otp']
            messages.success(request, 'OTP verified successfully.')
            return redirect('change_password')
        else:
            messages.error(request, 'Invalid OTP.')
            return render(request, 'verify_login_otp.html')
    return render(request, 'verify_login_otp.html')

def change_password(request):
    if request.method == 'POST':
        email = request.session.get('temp_email')
        new_password = request.POST.get('new_password')
        user = User.objects.filter(email=email).first()
        if user:
            user.set_password(new_password)
            user.save()
            del request.session['temp_email']
            messages.success(request, 'Password changed successfully.')
            return redirect('login')
        else:
            messages.error(request, 'User not found.')
            return render(request, 'change_password.html')
    return render(request, 'change_password.html')

def resend_otp(request):
    email = request.session.get('temp_email')
    user = User.objects.filter(email=email).first()
    if user:
        otp = random.randint(100000, 999999)
        request.session['otp'] = otp
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp}. Please use this code to proceed.',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        messages.success(request, 'OTP has been resent to your email.')
    else:
        messages.error(request, 'User not found.')
    return redirect(request.META.get('HTTP_REFERER', 'index'))