from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
def citizen_dashboard(request):
    return render(request,'citizen_dashboard.html')
def header(request):
    return render(request,'citizen_header.html')
def file_cases(request):
    return render(request,'file_cases.html')
def my_cases(request):
    return render(request,'my_cases.html')
def efilling(request):
    return render(request,'efilling.html')
def notification(request):
    return render(request,'notification.html')
def citizen_profile(request):
    return render(request,'citizen_profile.html')
def citizen_edit_profile(request):
    return render(request,'citizen_edit_profile.html')
