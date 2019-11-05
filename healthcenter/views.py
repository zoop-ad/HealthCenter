from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    return render(request, 'healthcenter/welcome.html')

@login_required(login_url='/accounts/login/')
def dashboard(request):
    return render(request,'healthcenter/dashboard.html')

def patient_registration(request):
    return render(request,'healthcenter/patientreg.html')

def register_patient(request):
    print(request.POST)

def opdreg(request):
    return render(request,'healthcenter/opdreg.html')