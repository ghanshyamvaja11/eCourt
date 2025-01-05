from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
def judge_dashboard(request):
    return render(request,'judge_dashboard.html')
def header(request):
    return render(request,'judge_header.html')
def judge_assigned_cases(request):
    return render(request,'judge_assigned_cases.html')
def judge_hearing(request):
    return render(request,'judge_hearing.html')
def outcome(request):
    return render(request,'outcome.html')
def case_doc(request):
    return render(request,'case_doc.html')
def judge_profile(request):
    return render(request,'judge_profile.html')
def judge_edit_profile(request):
    return render(request,'judge_edit_profile.html')
