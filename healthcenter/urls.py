from django.urls import path,include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard',views.dashboard),
    path('patientreg',views.patient_registration)
]

