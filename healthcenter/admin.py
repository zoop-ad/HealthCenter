from django.contrib import admin
from .models import Doctor,Patient,Employee,Timing,OPDRegistration,Feedback,MedicalDiagnosis,MedicineDistribution,Medicine, MedicinePurchase,MedicineStock,NewsArticle
# Register your models here.
admin.site.site_title = "MNNIT Health Center Admin"
admin.site.site_header = "MNNIT Health Center Admin"
admin.site.site_url = "/hc"

class PatientAdmin(admin.ModelAdmin):
    list_display = ('cardNo','name','contact_no','sex','emailid')

class TimingAdmin(admin.ModelAdmin):
    list_display = ('doc_name','day','in_time','out_time') 

    def doc_name(self, obj):
        if obj.dr:
            return [obj.dr.emp.first_name + ' ' +obj.dr.emp.last_name] 

    doc_name.short_description='Doctor Name'

class EmployeeAdmin(admin.ModelAdmin):
    list_display =('id','first_name','last_name','designation')


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('doc_name','specialization',)
    def doc_name(self, obj):
        if obj.emp:
            return [obj.emp.first_name + ' ' +obj.emp.last_name] 

    doc_name.short_description='Doctor Name'

class MedicalDiagnosisAdmin(admin.ModelAdmin):
    list_display = ('pat_name','timestamp','checked')
    def pat_name(self, obj):
        if obj.patient:
            return obj.patient.name 

    pat_name.short_description='Patient Name'

    def checked(self, obj):
        if obj.opd:
            return obj.opd.checked

    checked.short_description='Checked'

class OPDRegistrationAdmin(admin.ModelAdmin):
    list_display = ('id','pat_name','appoint_date','checked')

    def pat_name(self, obj):
        if obj.patient:
            return obj.patient.name 

    pat_name.short_description='Patient Name'

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name','email','rating','sentiment')

class MedicineAdmin(admin.ModelAdmin):
    list_display = ('id' , 'name','shortage_quantity')

class MedicineStockAdmin(admin.ModelAdmin):
    list_display = ('id','med_name','current_stock','expiry_date')

    def med_name(self,obj):
        if obj.medicine:
            return obj.medicine.name

admin.site.register(Employee,EmployeeAdmin)
admin.site.register(Patient,PatientAdmin)
admin.site.register(Timing,TimingAdmin)
admin.site.register(Doctor,DoctorAdmin)
admin.site.register(OPDRegistration,OPDRegistrationAdmin)
admin.site.register(Feedback,FeedbackAdmin)
admin.site.register(MedicalDiagnosis,MedicalDiagnosisAdmin)
admin.site.register(MedicineDistribution)
admin.site.register(Medicine,MedicineAdmin)
admin.site.register(MedicinePurchase)
admin.site.register(NewsArticle)
admin.site.register(MedicineStock,MedicineStockAdmin)