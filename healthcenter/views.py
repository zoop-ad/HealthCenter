from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Patient,Employee,Timing,OPDRegistration,Doctor,MedicalDiagnosis,Feedback
from django.http import HttpResponse, HttpResponseRedirect
from datetime import date
# Create your views here.

def index(request):
    return render(request, 'healthcenter/welcome.html')

@login_required(login_url='/accounts/login/')
def dashboard(request):
    if request.user.groups.all()[0].name=="Doctor":
        empl = get_object_or_404(Employee,pk=str(request.user))
        doc = Doctor.objects.filter(emp=empl)[0]
        today = date.today()
        opds = OPDRegistration.objects.filter(doctor=doc).filter(appoint_date=today)
        return render(request,'healthcenter/dashboard.html',{'msg':'Dr. ' + doc.emp.first_name + ' '+doc.emp.last_name , 'pat_list':opds})
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
    timings = Timing.objects.filter(dr=doc).filter(day=days)
    doc_list = Doctor.objects.all()
    return render(request,'healthcenter/docavail.html',{'times':timings,'docs':doc_list})

def diagnose(request):
    opdid = request.GET['opdid']
    opd = get_object_or_404(OPDRegistration,pk=opdid)
    pat = get_object_or_404(Patient,pk=opd.patient.cardNo)
    history = MedicalDiagnosis.objects.filter(patient=pat)
    return render(request,'healthcenter/diagnose.html',{'pat':pat,'history':history,'opdid':opdid,'cno':opd.patient.cardNo})

def diagnosepatient(request):
    opdid = request.GET['opdid']
    cno = request.GET['cno']
    opd = get_object_or_404(OPDRegistration,pk=opdid)
    pat = get_object_or_404(Patient,pk=opd.patient.cardNo)
    adv = request.POST['adv']
    bp =  request.POST['bp']
    weight = request.POST['wt']
    temp = request.POST['temp']
    dia = request.POST['dg']
    pres = request.POST['pc']
    path = request.POST['path']
    mdadvc = MedicalDiagnosis(patient=pat,opd=opd,advice=adv,bp=bp,weight=weight,temp=temp,diagnosis=dia,pres_given=pres,pathology=path)
    mdadvc.save()
    opd.checked=True
    opd.save()
    return HttpResponseRedirect('/hc/dashboard')

def feedback(request):
    return render(request,'healthcenter/feedback.html')

def submitfeedback(request):
    fb = Feedback(name=request.POST['name'],email=request.POST['email'],review=request.POST['review'],cleanliness=request.POST['radio'],med_availability=request.POST['radio1'],staff_behaviour=request.POST['radio2'],overall_satisfaction=request.POST['radio3'],rating=request.POST['rating'],suggestion=request.POST['suggestion'])
    fb.save()
    return HttpResponseRedirect('/hc')