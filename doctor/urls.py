from django.conf.urls import url
from . import views

app_name = 'doctor'
urlpatterns = [
    url(r'^doctor/(?P<doctor_id>[0-9]+)/$', views.homepage, name='homepage_doc'),
    url(r'^doctor/(?P<doctor_id>[0-9]+)/makeappointment/$', views.MakeAppointmentView.as_view(),
        name='make_appointment'),
    url(r'^doctor/(?P<doctor_id>[0-9]+)/patients$', views.PatientsPreviewView.as_view(), name='patients_preview'),
    url(r'^doctor/(?P<doctor_id>[0-9]+)/oldAppointments/$', views.OldAppointmentsView.as_view(),
        name='old_appointments'),
    url(r'^doctor/(?P<doctor_id>[0-9]+)/upcomingAppointments/$', views.UpcomingAppointmentsView.as_view(),
        name='upcoming_appointments'),
    url(r'^doctor/(?P<doctor_id>[0-9]+)/(?P<patient_id>[0-9]+)/$', views.patientDetails, name='patientDetails'),
    url(r'^doctor/(?P<doctor_id>[0-9]+)/appointment/(?P<appointment_id>[0-9]+)/$', views.appointment_details, name='appointment_details'),
    url(r'^doctor/(?P<doctor_id>[0-9]+)/appointment/(?P<appointment_id>[0-9]+)/addReport/', views.AddReportView.as_view(), name='add_report'),
    url(r'^ajax/get_times_available/$', views.get_times_available, name='times_available'),
    url(r'^ajax/remove_self_as_gp/$', views.remove_self_as_gp, name='remove_self_as_gp'),
    url(r'^ajax/add_self_as_gp/$', views.add_self_as_gp, name='add_self_as_gp'),
    url(r'^ajax/remove_report_from_appointment/$', views.remove_report_from_appointment, name='remove_report')
]

# /ajax/get_times_available/
