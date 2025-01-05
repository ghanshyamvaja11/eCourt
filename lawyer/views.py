from django.shortcuts import render

# Create your views here.
def lawyer_dashboard(request):
    return render(request,'lawyer_dashboard.html')
def header(request):
    return render(request,'lawyer_header.html')
def assigned_cases(request):
    return render(request,'assigned_cases.html')
def hearing(request):
    return render(request,'hearing.html')
def efilling(request):
    return render(request,'efilling.html')
def lawyer_profile(request):
    return render(request,'lawyer_profile.html')
def lawyer_edit_profile(request):
    return render(request,'lawyer_edit_profile.html')
