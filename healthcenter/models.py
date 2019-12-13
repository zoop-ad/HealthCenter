from django.db import models
from datetime import datetime
from django.utils.timezone import now
# Create your models here.

class Employee(models.Model):
    desg = (('Doctor','Doctor'),('Pharmacist','Pharmacist'),('Receptionist','Receptionist'))
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100,choices=desg,default="Doctor")

class Doctor(models.Model):
    emp = models.ForeignKey(Employee,on_delete=models.CASCADE,default=0)
    room_no = models.IntegerField()
    specialization = models.CharField(max_length=100)

class Timing(models.Model):
    DAYS =(('SUN','Sunday'),('MON','Monday'),('TUE','Tuesday'),('WED','Wednesday'),('THU','Thursday'),('FRI','Friday'),('SAT','Saturday'))
    dr = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    day = models.CharField(max_length=3,choices=DAYS)
    in_time = models.TimeField()
    out_time = models.TimeField()

class Patient(models.Model):
    cardNo = models.CharField(max_length=20,primary_key=True)
    name = models.CharField(max_length=100)
    dob = models.DateField()
    contact_no = models.IntegerField()
    address = models.CharField(max_length=500)
    validity = models.DateField()
    sex = models.CharField(max_length=1)
    blood_grp = models.CharField(max_length=5)

class OPDRegistration(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    appoint_date = models.DateField()
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    checked = models.BooleanField(default=False)
    checkup_time = models.TimeField(default=now)

class MedicalDiagnosis(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    opd = models.ForeignKey(OPDRegistration,on_delete=models.CASCADE)
    advice = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(default=now)
    bp = models.IntegerField()
    weight = models.IntegerField()
    temp = models.FloatField()
    diagnosis = models.CharField(max_length=1000)
    pres_given = models.CharField(max_length=1000)
    pathology = models.CharField(max_length=1000)
    med_given = models.BooleanField(default=False)

class Feedback(models.Model):
    params = (('Very Good','Very Good'),('Good','Good'),('Fair','Fair'),('Poor','Poor'))
    name = models.CharField(max_length=100)
    email = models.EmailField()
    review = models.CharField(max_length=5000)
    cleanliness = models.CharField(max_length=100,choices=params)
    med_availability = models.CharField(max_length=100,choices=params)
    staff_behaviour = models.CharField(max_length=100,choices=params)
    overall_satisfaction = models.CharField(max_length=100,choices=params)
    rating = models.IntegerField()
    suggestion = models.CharField(max_length=5000)
    otp = models.IntegerField(default=123456)
    verified = models.BooleanField(default=False)

class MedicineDistribution(models.Model):
    diagnosis = models.ForeignKey(MedicalDiagnosis,on_delete=models.CASCADE)
    medicine_name = models.CharField(max_length=100)
    quantity = models.IntegerField()

class Medicine(models.Model):
    med_name = models.CharField(max_length=100)
    cur_stock = models.IntegerField()