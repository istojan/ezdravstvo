from django.conf.urls import url
from . import views

app_name = 'patient'
urlpatterns = [
    url(r'^patient/(?P<patient_id>[0-9]+)/$', views.homepage, name='homepage'),
    url(r'^patient/(?P<patient_id>[0-9]+)/homepage/$', views.homepage, name='homepage'),
    url(r'^patient/(?P<patient_id>[0-9]+)/oldAppointments/$', views.old_appointments, name='old_appointments'),
    url(r'^patient/(?P<patient_id>[0-9]+)/upcomingAppointments', views.upcoming_appointments, name='upcoming_appointments'),
]
