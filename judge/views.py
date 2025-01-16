from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseBadRequest, JsonResponse
from users.models import *  # Import all models from users app
from cases.models import *  # Assuming there is a Case model in the cases app
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
def judge_hearings(request):
    # Clear all previous messages
    storage = messages.get_messages(request)
    storage.used = True

    judge = Judge.objects.get(user=request.user)

    hearings = Hearing.objects.filter(assigned_judge=judge, status='Scheduled')
    return render(request, 'judge_hearings.html', {'hearings': hearings})

@login_required(login_url='/login/')
def hearing_videocall_url(request):
    if request.method == "POST":
        hearing_id = request.POST.get("hearing_id")
        videocall_link = request.POST.get("videocall_url")
        if hearing_id and videocall_link:
            try:
                hearing = Hearing.objects.get(id=hearing_id)
                hearing.videocall_link = videocall_link
                hearing.save()

                messages.success(request, "Videocall URL submitted successfully.")

                hearing = Hearing.objects.get(id=hearing_id)

                case = Case.objects.get(id=hearing.case.id)
                Notification.objects.create(
                    user=case.plaintiff.user,
                    message=f'Join the Videocall link : {videocall_link} for hearing of case number : {case.case_number} on {hearing.date} before {hearing.time}.'
                )
                Notification.objects.create(
                    user=case.defendant.user,
                    message=f'Join the Videocall link : {videocall_link} for hearing of case number : {case.case_number} on {hearing.date} before {hearing.time}.'
                )
                Notification.objects.create(
                    user=case.assigned_lawyer.user,
                    message=f'Join the Videocall link : {videocall_link} for hearing of case number : {case.case_number} on {hearing.date} before {hearing.time}.'
                )
                Notification.objects.create(
                    user=case.defendant_lawyer.user,
                    message=f'Join the Videocall link : {videocall_link} for hearing of case number : {case.case_number} on {hearing.date} before {hearing.time}.'
                )
        
                messages.success(request, 'Hearing scheduled successfully.')
                subject = 'Hearing Scheduled'
                message = (
                    f"Please join the videoconference for the hearing of your case {case.case_number} as per the details below:\n\n"
                    f"Date: {hearing.date}\n"
                    f"Time: {hearing.time}\n\n"
                    f"Videocall Link: {videocall_link}\n\n"
                    f"Kindly ensure you are available at the scheduled time and join the hearing via the provided link.\n\n"
                    f"Best regards,\n"
                    f"The Court Team"
                )
                recipient_list = [case.plaintiff.user.email,
                                  case.defendant.user.email, case.assigned_lawyer.user.email, case.defendant_lawyer.user.email]
        
                send_mail(subject, message, 'ecourtofficially@gmail.com', recipient_list)
                
                return redirect('judge_hearings')  # Redirect to the judge's dashboard or another page
            except Hearing.DoesNotExist:
                messages.error(request, "Hearing not found.")
        else:
            messages.error(request, "Invalid form submission.")
    
    return redirect('judge_dashboard')  # Redirect to the judge's dashboard on failure

@login_required(login_url='/login/')
def submit_hearing_outcome(request):
    if request.method == "POST":
        hearing_id = request.POST.get("hearing_id")
        outcome = request.POST.get("outcome")

        if hearing_id and outcome:
            try:
                hearing = Hearing.objects.get(id=hearing_id)
                hearing.outcome = outcome
                hearing.save()

                messages.success(request, "Outcome submitted successfully.")
                # Redirect to the judge's dashboard or another page
                return redirect('judge_dashboard')
            except Hearing.DoesNotExist:
                messages.error(request, "Hearing not found.")
        else:
            messages.error(request, "Invalid form submission.")

    # Redirect to the judge's dashboard on failure
    return redirect('judge_dashboard')

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
            user=case.defendant,
            message=f'Outcome recorded for case {case.case_number}.'
        )
        Notification.objects.create(
            user=case.assigned_lawyer,
            message=f'Outcome recorded for case {case.case_number}.'
        )
        Notification.objects.create(
            user=case.defendant_lawyer,
            message=f'Outcome recorded for case {case.case_number}.'
        )

        messages.success(request, 'Outcome recorded successfully.')
        return redirect('outcome')

    return render(request, 'outcome.html', {'cases': cases})

@login_required(login_url='/login/')
def case_docs(request):
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
    return render(request, 'case_docs.html', {'documents': documents})

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
        user.full_name = request.POST.get('full_name')
        user.email = request.POST.get('email')
        user.contact_number = request.POST.get('contact_number')
        user.address = request.POST.get('address')
        # judge.court = request.POST.get('court')
        
        # Add validations
        if not user.full_name:
            messages.error(request, 'Name is required')
            return redirect('judge_profile')
        if not user.email:
            messages.error(request, 'Email is required')
            return redirect('judge_profile')
        if not user.contact_number:
            messages.error(request, 'Phone number is required')
            return redirect('judge_profile')
        if not user.address:
            messages.error(request, 'addrress is required')
            return redirect('judge_profile')
        # if not judge.court:
            # messages.error(request, 'Court is required')
            # return redirect('judge_profile')
        
         # Check for and save profile picture
        if request.FILES.get('profile_image'):
            profile_picture = request.FILES['profile_image']
            user.profile_picture = profile_picture

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
            user=case.defendant_lawyer.user,
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
                          case.defendant.user.email, case.assigned_lawyer.user.email, case.defendant_lawyer.user.email]

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
