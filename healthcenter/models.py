from django.db import models
from datetime import datetime,date
from django.utils.timezone import now
# Create your models here.

class Employee(models.Model):
    desg = (('Doctor','Doctor'),('Pharmacist','Pharmacist'),('Receptionist','Receptionist'))
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100,choices=desg,default="Doctor")

    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' - ' + self.designation

class Doctor(models.Model):
    emp = models.ForeignKey(Employee,on_delete=models.CASCADE,default=0)
    room_no = models.IntegerField()
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return self.emp.first_name + ' ' + self.emp.last_name + ' - ' + self.specialization

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
    contact_no = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    validity = models.DateField()
    sex = models.CharField(max_length=10)
    blood_grp = models.CharField(max_length=5)
    emailid = models.EmailField()
    password = models.CharField(max_length=1000)

    def __str__(self):
        return self.cardNo + ' - ' + self.name

class OPDRegistration(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    appoint_date = models.DateField()
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    checked = models.BooleanField(default=False)
    checkup_time = models.TimeField(default=now)
    is_live = models.BooleanField(default=False)
    registration_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return str(self.id) + '- ' + str(self.patient.name) + ' with Dr. '+ str(self.doctor.emp.first_name)

class MedicalDiagnosis(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    opd = models.ForeignKey(OPDRegistration,on_delete=models.CASCADE)
    advice = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(default=now)
    bp = models.CharField(max_length=1000)
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
    sentiment = models.CharField(max_length = 50, default='Positive')

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    authorized = models.BooleanField(default=True)
    shortage_quantity = models.IntegerField()

    def __str__(self):
        return str(self.id) + ' - ' +self.name
    
class MedicineDistribution(models.Model):
    diagnosis = models.ForeignKey(MedicalDiagnosis,on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine,on_delete=models.CASCADE)
    quantity = models.IntegerField()

class MedicineStock(models.Model):
    medicine = models.ForeignKey(Medicine,on_delete=models.CASCADE)
    current_stock = models.IntegerField()
    expiry_date = models.DateField()

class MedicinePurchase(models.Model):
    medicine = models.ForeignKey(Medicine,on_delete=models.CASCADE)
    purchased_from = models.CharField(max_length=1000)
    purchase_order_no = models.IntegerField()
    purchase_order_date = models.DateField()
    bill_no = models.IntegerField()
    billing_date = models.DateField()
    medicine_quantity = models.IntegerField()
    amount = models.DecimalField(max_digits=1000,decimal_places=10)
    mf_date = models.DateField()
    expiry_date = models.DateField()
    timestamp = models.DateTimeField(default=now)

class PathologyTest(models.Model):
    test_name = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.id) + ' - ' +self.name   

class PathologyTestReports(models.Model):
    diagnosis = models.ForeignKey(MedicalDiagnosis,on_delete=models.CASCADE) 
    test = models.ForeignKey(PathologyTest,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=now)
    result = models.CharField(max_length=1000)

class NewsArticle(models.Model):
    headline = models.CharField(max_length=1000)
    link = models.CharField(max_length=1000)