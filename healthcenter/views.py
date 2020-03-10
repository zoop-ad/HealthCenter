from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from django.contrib.auth.decorators import login_required
from .models import Patient,Employee,Timing,OPDRegistration,Doctor,MedicalDiagnosis,Feedback,MedicineDistribution
from django.http import HttpResponse, HttpResponseRedirect
from datetime import date
from django.core.mail import send_mail
from random import randint
import datetime
# Create your views here.

def index(request):
    return render(request, 'healthcenter/front.html')

@login_required(login_url='/accounts/login/')
def dashboard(request):
    if request.user.groups.all()[0].name=="Doctor":
        empl = get_object_or_404(Employee,pk=str(request.user))
        doc = Doctor.objects.filter(emp=empl)[0]
        today = date.today()
        opds = OPDRegistration.objects.filter(doctor=doc).filter(appoint_date=today)
        return render(request,'healthcenter/doctor-dashboard.html',{'msg':'Dr. ' + doc.emp.first_name + ' '+doc.emp.last_name , 'pat_list':opds})
    else:
        pst = get_object_or_404(Employee,pk=str(request.user))
        print(pst)
        dgs = MedicalDiagnosis.objects.filter(med_given=False)
        print(dgs)
        return render(request,'healthcenter/pharmacist-dashboard.html',{'msg':'Pharmacist '+pst.first_name + ' '+pst.last_name,'dgs':dgs})

def patient_registration(request):
    return render(request,'healthcenter/patientreg.html')

def register_patient(request):
    np = Patient(cardNo=request.POST['cardno'],name=request.POST['fname'],dob=request.POST['dob'],contact_no=request.POST['cno'],address=request.POST['addr'],validity=request.POST['validity'],sex=request.POST['sex'],blood_grp=request.POST['bg'])
    np.save()
    return render(request,'healthcenter/front.html',{'msg':'Patient ' +request.POST['cardno']+' is successfully registered.'})

def opdreg(request):
    doc_list = Doctor.objects.all()
    return render(request,'healthcenter/opdreg.html',{'docs':doc_list})

def regopd(request):
    card = request.POST['cardno']
    drno = request.POST['docreq']
    dt = request.POST['dateofreg']
    year,month,day = dt.split('-')
    day_name = datetime.date(int(year), int(month), int(day)).strftime("%A").upper()[0:3]
    try:
        pat = get_object_or_404(Patient,pk=card)
        doc = get_object_or_404(Doctor,pk=drno)
    except:
        doc_list = Doctor.objects.all()
        return render(request,'healthcenter/opdreg.html',{'docs':doc_list,'err':'Patient not registered'})
    try:
        tim = get_list_or_404(Timing,dr=doc,day=day_name)
    except:
        doc_list = Doctor.objects.all()
        return render(request,'healthcenter/opdreg.html',{'docs':doc_list,'err':'Doctor not available on given date'})
    print(tim)
    reg = OPDRegistration(patient=pat,appoint_date=request.POST['dateofreg'],doctor=doc,checked=False)
    reg.save()
    return render(request,'healthcenter/front.html',{'msg':'Successfully Registered for OPD on '+request.POST['dateofreg']+' with Dr. '+ doc.emp.first_name + ' '+doc.emp.last_name})

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
    nm = 'Dr. '+doc.emp.first_name + ' ' + doc.emp.last_name
    return render(request,'healthcenter/docavail.html',{'times':timings,'docs':doc_list,'docname':nm})

def diagnose(request):
    opdid = request.GET['opdid']
    opd = get_object_or_404(OPDRegistration,pk=opdid)
    pat = get_object_or_404(Patient,pk=opd.patient.cardNo)
    history = MedicalDiagnosis.objects.filter(patient=pat)
    if len(history)>5:
        history=history[0:5]
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
    otp = randint(100000,999999)
    fb = Feedback(name=request.POST['name'],email=request.POST['email'],review=request.POST['review'],cleanliness=request.POST['radio'],med_availability=request.POST['radio1'],staff_behaviour=request.POST['radio2'],overall_satisfaction=request.POST['radio3'],rating=request.POST['rating'],suggestion=request.POST['suggestion'],otp=otp,verified=False)
    fb.save()    
    send_mail('MNNIT Health Center Feedback Verification OTP','Your OTP is - '+str(otp),'amulya@mnnit.ac.in',[str(fb.email)],fail_silently=False)
    return render(request,'healthcenter/verify.html',{'em':fb.email,'fbid':fb.id,'fl':1})

def gethistory(request):
    print(request.GET)
    cno = request.GET['cno']
    print(cno)
    pat = get_object_or_404(Patient,pk=cno)
    history = MedicalDiagnosis.objects.filter(patient=pat)
    return render(request,'healthcenter/history.html',{'history':history,'pat':pat})

def distribute(request):
    dgsid = request.GET['dgsid']
    dgs = get_object_or_404(MedicalDiagnosis,pk=dgsid)
    print(dgs)
    return render(request,'healthcenter/distribute.html',{'dgsid':dgsid,'dgs':dgs})

def distributemed(request):
    dgsid = request.GET['dgsid']
    dgs = get_object_or_404(MedicalDiagnosis,pk=dgsid)
    meds = request.POST.getlist('meds')
    qty = request.POST.getlist('qty')
    dgs.med_given=True
    dgs.save()
    i=0
    while i<len(meds):
        medd = MedicineDistribution(diagnosis=dgs,medicine_name=meds[i],quantity=qty[i])
        medd.save()
        i+=1
    return HttpResponseRedirect('/hc/dashboard')

def verifyOTP(request):
    fbid = request.GET['fbid']
    fb = get_object_or_404(Feedback,pk=fbid)
    otp = int(str(request.POST['d1'])+str(request.POST['d2'])+str(request.POST['d3'])+str(request.POST['d4'])+str(request.POST['d5'])+str(request.POST['d6']))
    if otp==fb.otp:
        fb.verified=True
        fb.save()
        return render(request,'healthcenter/thanks.html')
    else:
        return render(request,'healthcenter/verify.html',{'em':fb.email,'fbid':fb.id,'fl':2})

def ffront(request):
    return render(request,'healthcenter/front.html')     