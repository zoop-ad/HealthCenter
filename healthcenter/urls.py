from django.urls import path,include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard',views.dashboard),
    path('patientreg',views.patient_registration),
    path('registerpatient',views.register_patient),
    path('opdreg',views.opdreg),
    path('regopd',views.regopd),
    path('medavail',views.medavail),
    path('docavail',views.docavail),
    path('docavailcheck',views.docavailcheck),
    path('diagnose',views.diagnose),
    path('diagnosepatient',views.diagnosepatient),
    path('feedback',views.feedback),
    path('submitfeedback',views.submitfeedback),
    path('gethistory',views.gethistory)
]

