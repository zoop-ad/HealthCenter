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
    path('medavailcheck',views.medavailcheck),
    path('diagnose',views.diagnose),
    path('diagnosepatient',views.diagnosepatient),
    path('feedback',views.feedback),
    path('submitfeedback',views.submitfeedback),
    path('gethistory',views.gethistory),
    path('distribute',views.distribute),
    path('distributemed',views.distributemed),
    path('verifyotp',views.verifyOTP),
    path('checkhis',views.checkhist),
    path('viewhis',views.checkhis),
    path('graph',views.showgraph),
    path('viewgraph',views.viewgraph),
    path('makelive',views.makelive),
    path('transfer',views.transfer),
    path('transferpatient',views.transferpatient),
    path('fbsv',views.fbsv),
    path('tall',views.tagallfb),
    path('seepatlist',views.seepatlist)
]