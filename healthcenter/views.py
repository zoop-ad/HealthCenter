from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Patient,Employee,Timing,OPDRegistration,Doctor
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.

def index(request):
    return render(request, 'healthcenter/welcome.html')

@login_required(login_url='/accounts/login/')
def dashboard(request):
    if request.user.groups.all()[0].name=="Doctor":
        return render(request,'healthcenter/dashboard.html',{'msg':'Hello Doctor '+str(request.user)})
    elif request.user.groups.all()[0].name=="Pharmacist":
        return render(request,'healthcenter/dashboard.html',{'msg':'Hello Pharmacist '+str(request.user)})    

def patient_registration(request):
    return render(request,'healthcenter/patientreg.html')

def register_patient(request):
    np = Patient(cardNo=request.POST['cardno'],name=request.POST['fname'],dob=request.POST['dob'],contact_no=request.POST['cno'],address=request.POST['addr'],validity=request.POST['validity'],sex=request.POST['sex'],blood_grp=request.POST['bg'])
    np.save()
    return HttpResponseRedirect('/hc/')

def opdreg(request):
    doc_list = Doctor.objects.all()
    return render(request,'healthcenter/opdreg.html',{'docs':doc_list})

def regopd(request):
    card = request.POST['cardno']
    drno = request.POST['docreq']
    pat = get_object_or_404(Patient,pk=card)
    doc = get_object_or_404(Doctor,pk=drno)
    reg = OPDRegistration(patient=pat,appoint_date=request.POST['dateofreg'],doctor=doc,checked=False)
    reg.save()
    return HttpResponseRedirect('/hc/')

def medavail(request):
    return render(request,'healthcenter/medavail.html')

def docavail(request):
    doc_list = Doctor.objects.all()
    return render(request,'healthcenter/docavail.html',{'docs':doc_list,'times':[]})

def docavailcheck(request):
    drno = request.POST['docreq']
    doc = get_object_or_404(Doctor,pk=drno)
    days = request.POST['day']
    timings = Timing.objects.filter(dr=doc.emp).filter(day=days)
    print(timings)
    doc_list = Doctor.objects.all()
    return render(request,'healthcenter/docavail.html',{'times':timings,'docs':doc_list})