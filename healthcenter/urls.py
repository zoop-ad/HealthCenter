from django.urls import path,include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard',views.dashboard),
    path('patientreg',views.patient_registration),
    path('registerpatient',views.register_patient),
    path('opdreg',views.opdreg),
    path('medavail',views.medavail),
    path('docavail',views.docavail)
]

