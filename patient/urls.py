from django.conf.urls import url

from patient import utils
from . import views

app_name = 'patient'
urlpatterns = [
    url(r'^patient/(?P<patient_id>[0-9]+)/$', views.homepage, name='homepage'),
    url(r'^patient/(?P<patient_id>[0-9]+)/homepage/$', views.homepage, name='homepage'),
    url(r'^patient/(?P<patient_id>[0-9]+)/oldAppointments/$', views.old_appointments, name='old_appointments'),
    url(r'^patient/(?P<patient_id>[0-9]+)/upcomingAppointments', views.upcoming_appointments, name='upcoming_appointments'),
    url(r'^patient/(?P<patient_id>[0-9]+)/appointment/(?P<appointment_id>[0-9]+)/$', views.appointment_details, name='appointment_details'),
    url(r'^ajax/get_patient_personal_info/$', utils.get_patient_personal_info, name='get_patient_personal_info'),
    url(r'^ajax/get_old_appointments/$', utils.get_old_appointments, name='get_old_appointments'),
    url(r'^ajax/get_upcoming_appointments/$', utils.get_upcoming_appointments, name='get_upcoming_appointments'),
]
