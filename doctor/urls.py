from django.conf.urls import url
from . import views


app_name = 'doctor'
urlpatterns = [
    url(r'^doctor/(?P<doctor_id>[0-9]+)/$', views.homepage, name='homepage_doc'),
    url(r'^doctor/(?P<doctor_id>[0-9]+)/makeappointment/$', views.MakeAppointmentView.as_view(), name='make_appointment'),
    url(r'^doctor/(?P<doctor_id>[0-9]+)/patients$', views.PatientsPreviewView.as_view(), name='patients_preview')
    # url(r'^patient/(?P<patient_id>[0-9]+)/homepage/$', views.homepage, name='homepage'),
    # url(r'^patient/(?P<patient_id>[0-9]+)/oldAppointments/$', views.old_appointments, name='old_appointments'),
    # url(r'^patient/(?P<patient_id>[0-9]+)/upcomingAppointments', views.upcoming_appointments, name='upcoming_appointments'),
]

