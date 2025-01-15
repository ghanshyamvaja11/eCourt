from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseBadRequest, JsonResponse
from users.models import *  # Import all models from users app
from cases.models import Case, Hearing  # Assuming there is a Case model in the cases app
from notifications.models import *  # Assuming there is a Notification model in the notifications app
from django.core.mail import send_mail
from django.contrib.auth import logout

@login_required(login_url='/login/')
def judge_dashboard(request):
    # Clear all previous messages
    storage = messages.get_messages(request)
    storage.used = True

    return render(request, 'judge_dashboard.html')

@login_required(login_url='/login/')
def judge_assigned_cases(request):
    # Clear all previous messages
    storage = messages.get_messages(request)
    storage.used = True

    judge = Judge.objects.get(user=request.user)
    cases = Case.objects.filter(assigned_judge=judge)
    return render(request, 'judge_assigned_cases.html', {'cases': cases})

def update_case_status(request):
    try:
        case_id = request.POST.get('case_id')
        new_status = request.POST.get('new_status')
        # Fetch the case
        case = Case.objects.get(id=case_id)
        case.status = new_status
        case.save()
        return redirect('judge_assigned_cases')
    except:
        return redirect('judge_assigned_cases')

@login_required(login_url='/login/')
def judge_hearing(request):
    # Clear all previous messages
    storage = messages.get_messages(request)
    storage.used = True

    judge = Judge.objects.get(user=request.user)

    hearings = Hearing.objects.filter(assigned_judge=judge, status='Scheduled')
    print(hearings)
    return render(request, 'judge_hearing.html', {'hearings': hearings})

@login_required(login_url='/login/')
def outcome(request):
    judge = Judge.objects.get(user=request.user)
    cases = Case.objects.filter(assigned_judge=judge)

    if request.method == 'POST':
        case_id = request.POST.get('case_id')
        outcome_text = request.POST.get('outcome')

        case = get_object_or_404(Case, id=case_id)
        case.status = 'CLOSED'
        case.save()

        Hearing.objects.filter(case=case).update(outcome=outcome_text)

        Notification.objects.create(    
            user=case.plantiff,
            message=f'Outcome recorded for case {case.case_number}.'
        )
        Notification.objects.create(
            user=case.defendent,
            message=f'Outcome recorded for case {case.case_number}.'
        )
        Notification.objects.create(
            user=case.assigned_lawyer,
            message=f'Outcome recorded for case {case.case_number}.'
        )
        Notification.objects.create(
            user=case.defendent_lawyer,
            message=f'Outcome recorded for case {case.case_number}.'
        )

        messages.success(request, 'Outcome recorded successfully.')
        return redirect('outcome')

    return render(request, 'outcome.html', {'cases': cases})

@login_required(login_url='/login/')
def case_doc(request):
    # Clear all previous messages
    storage = messages.get_messages(request)
    storage.used = True

    judge = Judge.objects.get(user=request.user)
    cases = Case.objects.filter(assigned_judge=judge)
    return render(request, 'case_doc.html', {'cases': cases})

@login_required(login_url='/login/')
def judge_profile(request):
    # Clear all previous messages
    storage = messages.get_messages(request)
    storage.used = True

    judge = Judge.objects.get(user=request.user)
    user = User.objects.get(id=judge.user.id)
    return render(request, 'judge_profile.html', {'judge': judge, 'user': user})

@login_required(login_url='/login/')
def judge_edit_profile(request):
    # Clear all previous messages
    storage = messages.get_messages(request)
    storage.used = True

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
        
         # Check for and save profile picture
        if request.FILES.get('profile_image'):
            profile_picture = request.FILES['profile_image']
            user.profile_picture = profile_picture
        
        judge.save()
        user.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('judge_profile')
        
    return render(request, 'judge_edit_profile.html', {'judge': judge, 'user': user})

@login_required(login_url='/login/')
def schedule_hearing(request):
    judge = Judge.objects.get(user=request.user)
    cases = Case.objects.filter(assigned_judge=judge)

    if request.method == 'POST':
        case_id = request.POST.get('case_id')
        date = request.POST.get('date')
        time = request.POST.get('time')
        # videocall_link = request.POST.get('videocall_link')

        case = get_object_or_404(Case, id=case_id)
        judge = Judge.objects.get(user = request.user)
        Hearing.objects.create(
            case=case,
            date=date,
            time=time,
            assigned_judge = judge
        )

        Notification.objects.create(
            user=case.plaintiff.user,
            message=f'Hearing scheduled for case {case.case_number} on {date} at {time}.'
        )
        Notification.objects.create(
            user=case.defendant.user,
            message=f'Hearing scheduled for case {case.case_number} on {date} at {time}.'
        )
        Notification.objects.create(
            user=case.assigned_lawyer.user,
            message=f'Hearing scheduled for case {case.case_number} on {date} at {time}.'
        )
        Notification.objects.create(
            user=case.defendent_lawyer.user,
            message=f'Hearing scheduled for case {case.case_number} on {date} at {time}.'
        )

        messages.success(request, 'Hearing scheduled successfully.')
        subject = 'Hearing Scheduled'
        message = (
            f"A hearing has been scheduled for your case {case.case_number}.\n\n"
            f"Date: {date}\nTime: {time}\n\n"
            f"A video call link will be provided 15 to 20 minutes before the scheduled time.\n\n"
            f"Please be available and check your notifications or email for the link prior to the hearing."
        )
        recipient_list = [case.plaintiff.user.email,
                          case.defendant.user.email, case.assigned_lawyer.user.email, case.defendent_lawyer.user.email]

        send_mail(subject, message, 'ecourtofficially@gmail.com', recipient_list)

        return redirect('schedule_hearing')

    return render(request, 'schedule_hearing.html', {'cases': cases})

@login_required(login_url='/login/')
def notifications(request):
    # Clear all previous messages
    storage = messages.get_messages(request)
    storage.used = True
    
    judge = Judge.objects.get(user=request.user)
    notifications = Notification.objects.filter(user=judge.user).order_by('-timestamp')
    return render(request, 'notification.html', {'notifications': notifications})

@login_required(login_url='/login/')
def logout_view(request):
    # Clear all previous messages
    storage = messages.get_messages(request)
    storage.used = True

    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')
