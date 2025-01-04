from django.shortcuts import render

# Create your views here.
def dashbord(request):
    return render(request,'admin_dashbord.html')
def header(request):
    return render(request,'admin_header.html')
def user_management(request):
    return render(request,'user_management.html')
   
def  citizens_management(request):
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
    