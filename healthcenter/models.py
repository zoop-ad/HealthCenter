from django.db import models

# Create your models here.

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

class Doctor(models.Model):
    emp_id = models.ForeignKey(Employee,on_delete=models.CASCADE,default=0)
    room_no = models.IntegerField()
    specialization = models.CharField(max_length=100)

class Timing(models.Model):
    DAYS =(('SUN','Sunday'),('MON','Monday'),('TUE','Tuesday'),('WED','Wednesday'),('THU','Thursday'),('FRI','Friday'),('SAT','Saturday'))
    dr_id = models.ForeignKey(Employee,on_delete=models.CASCADE)
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
    blood_grp = models.CharField(max_length=2)