from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from django.contrib.auth.decorators import login_required
from .models import Patient,Employee,Timing,OPDRegistration,Doctor,MedicalDiagnosis,Feedback,MedicineDistribution,Medicine,MedicineStock,NewsArticle
from django.http import HttpResponse, HttpResponseRedirect
from datetime import date
from django.core.mail import send_mail
from random import randint
import datetime
import io
from django.http import FileResponse
from django.views.generic import View
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.db.models import Q
from monkeylearn import MonkeyLearn
# Create your views here.

def index(request):
    art = NewsArticle.objects.all()
    return render(request, 'healthcenter/front.html',{'art':art})

@login_required(login_url='/accounts/login/')
def dashboard(request):
    if request.user.groups.all()[0].name=="Doctor":
        empl = get_object_or_404(Employee,pk=str(request.user))
        doc = Doctor.objects.filter(emp=empl)[0]
        doclis = Doctor.objects.filter(~Q(emp=empl))
        today = date.today()
        opds = OPDRegistration.objects.filter(doctor=doc).filter(checked=False).filter(is_live=False)
        lopds = OPDRegistration.objects.filter(doctor=doc).filter(checked=False).filter(is_live=True)
        return render(request,'healthcenter/doctor-dashboard.html',{'doc':doc,'doclis':doclis,'msg':'Dr. ' + doc.emp.first_name + ' '+doc.emp.last_name , 'pat_list':opds,'live_pat_list':lopds})
    elif request.user.groups.all()[0].name=="Pharmacist":
        pst = get_object_or_404(Employee,pk=str(request.user))
        dgs = MedicalDiagnosis.objects.filter(med_given=False)
        return render(request,'healthcenter/pharmacist-dashboard.html',{'msg':'Pharmacist '+pst.first_name + ' '+pst.last_name,'dgs':dgs})
    else:
        recp = get_object_or_404(Employee,pk=str(request.user))
        opdss = OPDRegistration.objects.filter(checked=False)
        return render(request,'healthcenter/recep-dash.html',{'msg':'Receptionist '+recp.first_name+' '+recp.last_name,'opds':opdss})

def patient_registration(request):
    return render(request,'healthcenter/patientreg.html')

def register_patient(request):
    np = Patient(cardNo=request.POST['cardno'],name=request.POST['fname'],dob=request.POST['dob'],contact_no=request.POST['cno'],address=request.POST['addr'],validity=request.POST['validity'],sex=request.POST['sex'],blood_grp=request.POST['bg'],emailid=request.POST['eml'],password=request.POST['eml'])
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
    reg = OPDRegistration(patient=pat,appoint_date=request.POST['dateofreg'],doctor=doc,checked=False)
    reg.save()
    return render(request,'healthcenter/front.html',{'msg':'Successfully Registered for OPD on '+request.POST['dateofreg']+' with Dr. '+ doc.emp.first_name + ' '+doc.emp.last_name + ' OPD ID = '+str(reg.id)})

def medavail(request):
    return render(request,'healthcenter/medavail.html')

def docavail(request):
    doc_list = Doctor.objects.all()
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_id_list = []
    for session in active_sessions:
        data = session.get_decoded()
        user_id_list.append(data.get('_auth_user_id', None))
    # Query all logged in users based on id list
    xx= User.objects.filter(id__in=user_id_list)
    yy=[]
    for x in xx:
        if x.groups.filter(name='Doctor').exists():
            yy.append(x)
    return render(request,'healthcenter/docavail.html',{'docs':doc_list,'times':[],'yy':yy})

def docavailcheck(request):
    drno = request.POST['docreq']
    doc = get_object_or_404(Doctor,pk=drno)
    days = request.POST['day']
    timings = Timing.objects.filter(dr=doc).filter(day=days)
    doc_list = Doctor.objects.all()
    nm = 'Dr. '+doc.emp.first_name + ' ' + doc.emp.last_name
    return render(request,'healthcenter/docavail.html',{'times':timings,'docs':doc_list,'docname':nm,'yy':[]})

def medavailcheck(request):
    med = request.POST['med']
    try:
        medicine_obj = Medicine.objects.get(name=med)
    except:
        return render(request,'healthcenter/medavail.html',{'err':'No such medicine exists'})
    try:
        stck = get_list_or_404(MedicineStock,medicine = medicine_obj)
    except:
        return render(request,'healthcenter/medavail.html',{'msg':'Not Available','stck':[{'current_stock':0,'expiry_date':'NA'}],'medname':med})
    return render(request,'healthcenter/medavail.html',{'msg':'Available','stck':stck,'medname':med})

def transfer(request):
    opdid = request.GET['opdid']
    opd = get_object_or_404(OPDRegistration,pk=opdid)
    pat = get_object_or_404(Patient,pk=opd.patient.cardNo)
    doclis = Doctor.objects.all()
    return render(request,'healthcenter/transfer.html',{'doclis':doclis,'pat':pat,'opdid':opdid})

def diagnose(request):
    opdid = request.GET['opdid']
    opd = get_object_or_404(OPDRegistration,pk=opdid)
    pat = get_object_or_404(Patient,pk=opd.patient.cardNo)
    history = MedicalDiagnosis.objects.filter(patient=pat)
    if len(history)>5:
        history=history[0:5]
    return render(request,'healthcenter/diagnose.html',{'pat':pat,'history':history,'opdid':opdid,'cno':opd.patient.cardNo})

def transferpatient(request):
    opdid = request.GET['opdid']
    opd = get_object_or_404(OPDRegistration,pk=opdid)
    drID = request.POST['docreq']
    doc = get_object_or_404(Doctor,pk=drID)
    opd.doctor = doc
    opd.save()
    return HttpResponseRedirect('/hc/dashboard')

def diagnosepatient(request):
    opdid = request.GET['opdid']
    cno = request.GET['cno']
    opd = get_object_or_404(OPDRegistration,pk=opdid)
    pat = get_object_or_404(Patient,pk=opd.patient.cardNo)
    adv = request.POST['adv']
    systo = request.POST['systo']
    diasto = request.POST['diasto']
    bp = systo + ' ' + diasto
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
    send_mail('MNNIT Health Center Feedback Verification OTP','Your OTP is - '+str(otp),'healthcenter@mnnit.ac.in',[str(fb.email)],fail_silently=False)
    return render(request,'healthcenter/verify.html',{'em':fb.email,'fbid':fb.id,'fl':1})

def gethistory(request):
    cno = request.GET['cno']
    pat = get_object_or_404(Patient,pk=cno)
    history = MedicalDiagnosis.objects.filter(patient=pat)
    return render(request,'healthcenter/history.html',{'history':history,'pat':pat})

def distribute(request):
    dgsid = request.GET['dgsid']
    dgs = get_object_or_404(MedicalDiagnosis,pk=dgsid)
    return render(request,'healthcenter/distribute.html',{'dgsid':dgsid,'dgs':dgs})

def distributemed(request):
    dgsid = request.GET['dgsid']
    dgs = get_object_or_404(MedicalDiagnosis,pk=dgsid)
    meds = request.POST.getlist('meds')
    qty = request.POST.getlist('qty')
    i=0
    while i<len(meds):
        try:
            medicine_obj = Medicine.objects.get(name=meds[i])
            medicine_stock_obj = MedicineStock.objects.get(medicine=medicine_obj)
        except:
            return render(request,'healthcenter/distribute.html',{'dgsid':dgsid,'dgs':dgs})
        if medicine_stock_obj.current_stock>=int(qty[i]):
            medicine_stock_obj.current_stock -= int(qty[i])
        medicine_stock_obj.save()
        medd = MedicineDistribution(diagnosis=dgs,medicine=medicine_obj,quantity=qty[i])
        medd.save()
        i+=1
    dgs.med_given=True
    dgs.save()
    mq =zip(meds,qty)
    html_message = render_to_string('healthcenter/receipt.html',{'dgs':dgs,'pat':dgs.patient,'mq':mq})
    send_mail("MNNIT Health Center OPD Receipt","",'healthcenter@mnnit.ac.in',[str(dgs.patient.emailid)],fail_silently=False,html_message=html_message)
    return render(request,'healthcenter/front.html',{'msg':'Medicine Distributed successfully!'})

def verifyOTP(request):
    fbid = request.GET['fbid']
    fb = get_object_or_404(Feedback,pk=fbid)
    otp = int(str(request.POST['d1'])+str(request.POST['d2'])+str(request.POST['d3'])+str(request.POST['d4'])+str(request.POST['d5'])+str(request.POST['d6']))
    if otp==fb.otp:
        fb.verified=True
        ml = MonkeyLearn('2996cb83b0f2c42cdd8d5785a11d5609b7db736d')
        data = [fb.review]
        model_id = 'cl_pi3C7JiL'
        result = ml.classifiers.classify(model_id, data)
        fb.sentiment = result.body[0]["classifications"][0]["tag_name"]
        fb.save()
        return render(request,'healthcenter/thanks.html')
    else:
        return render(request,'healthcenter/verify.html',{'em':fb.email,'fbid':fb.id,'fl':2})

def checkhis(request):
    cno = request.POST['cno']
    password = request.POST['password']
    pat = get_object_or_404(Patient,pk=cno)
    if password == pat.password:
        history = MedicalDiagnosis.objects.filter(patient=pat)
        return render(request,'healthcenter/history.html',{'history':history,'pat':pat})
    else:
        return render(request,'healthcenter/patlogin.html',{'msg':'Incorrect username or password.'})

def checkhist(request):
    return render(request,'healthcenter/patlogin.html')

@staff_member_required
def showgraph(request):
    return render(request,'healthcenter/graph.html')

@staff_member_required
def viewgraph(request):
    sd = request.POST["sd"].split('/')
    ed = request.POST["ed"].split('/')
    sdate = str(sd[2]) + '-'+str(sd[1])+ '-' +str(sd[0])
    edate = str(ed[2]) + '-'+str(ed[1])+ '-' +str(ed[0])
    opds = OPDRegistration.objects.filter(appoint_date__range=[sdate,edate])
    presc = MedicineDistribution.objects.filter(diagnosis__opd__appoint_date__range=[sdate,edate])
    meds = {}
    mapp = {}
    mapspec= {}
    for i in opds:
        docname = 'Dr. '+i.doctor.emp.first_name + ' '+ i.doctor.emp.last_name  
        if docname in mapp.keys():
            xx = mapp[docname]
            xx+=1
            mapp[docname] =xx
        else:
            mapp[docname]=1
    for j in opds:
        docspec = j.doctor.specialization
        if docspec in mapspec.keys():
            xx = mapspec[docspec]
            xx+=1
            mapspec[docspec] =xx
        else:
            mapspec[docspec]=1
    for k in presc:
        medicine = k.medicine.name
        if medicine in meds.keys():
            xx = meds[medicine]
            xx+=1
            meds[medicine]=xx
        else:
            meds[medicine]=1 
    return render(request,'healthcenter/dgraph.html',{'docs':list(mapp.keys()),'count':list(mapp.values()),'specs':list(mapspec.keys()),'meds':list(meds.keys()),'medscount':list(meds.values())})

def makelive(request):
    opdr = get_object_or_404(OPDRegistration,pk=request.GET['opdid'])
    opdr.is_live=True
    opdr.save()
    return HttpResponseRedirect('/hc/dashboard')

def fbsv(request):
    fb = Feedback.objects.all()
    cl = {'Poor':0,'Fair':0,'Good':0,'Very Good':0}
    med = {'Poor':0,'Fair':0,'Good':0,'Very Good':0}
    staff = {'Poor':0,'Fair':0,'Good':0,'Very Good':0}
    sat = {'Poor':0,'Fair':0,'Good':0,'Very Good':0}
    rat = {1:0,2:0,3:0,4:0,5:0}
    sen = {'Positive':0,'Negative':0,'Neutral':0}
    for x in fb:
        cl[x.cleanliness]+=1
        med[x.med_availability]+=1
        staff[x.staff_behaviour]+=1
        sat[x.overall_satisfaction]+=1
        rat[x.rating]+=1
        sen[x.sentiment]+=1
    return render(request,'healthcenter/fbgraph.html',{'cl':list(cl.values()),'med':list(med.values()),'staff':list(staff.values()),'sat':list(sat.values()),'rat':list(rat.values()),'sen':list(sen.values())})

def tagallfb(request):
    fb = Feedback.objects.all()
    ml = MonkeyLearn('2996cb83b0f2c42cdd8d5785a11d5609b7db736d')
    model_id = 'cl_pi3C7JiL'
    for x in fb:
        data = [x.review]
        result = ml.classifiers.classify(model_id, data)
        x.sentiment = result.body[0]["classifications"][0]["tag_name"]
        print(x.review , ' ',x.sentiment)
        x.save()
    return HttpResponseRedirect('/hc')

def seepatlist(request):
    dt=request.POST["dt"].split('/')
    date = str(dt[2]) + '-'+str(dt[1])+ '-' +str(dt[0])
    visibledate = str(dt[0]) + '-'+str(dt[1])+ '-' +str(dt[2])
    docid=request.GET['docid']
    doc=get_object_or_404(Doctor,pk=docid)
    opds=OPDRegistration.objects.filter(doctor=doc).filter(appoint_date=date)
    return render(request,'healthcenter/seepatlist.html',{'nomenclature':'Dr. ' + doc.emp.first_name + ' '+doc.emp.last_name,'date':visibledate,'opds':opds})