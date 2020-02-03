from django.contrib import admin
from .models import Doctor,Patient,Employee,Timing,OPDRegistration,Feedback,MedicalDiagnosis,MedicineDistribution
# Register your models here.
admin.site.site_title = "MNNIT Health Center Admin"
admin.site.site_header = "MNNIT Health Center Admin"
admin.site.site_url = "/hc"

class PatientAdmin(admin.ModelAdmin):
    list_display = ('cardNo','name','contact_no')


admin.site.register(Patient,PatientAdmin)
admin.site.register(Timing)

class EmployeeAdmin(admin.ModelAdmin):
    list_display =('id','first_name','last_name')

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('emp_id','specialization')

admin.site.register(Employee,EmployeeAdmin)
admin.site.register(Doctor,DoctorAdmin)
admin.site.register(OPDRegistration)
admin.site.register(Feedback)
admin.site.register(MedicalDiagnosis)
admin.site.register(MedicineDistribution)