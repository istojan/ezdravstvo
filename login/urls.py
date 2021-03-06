from django.conf.urls import url

from login import utils
from . import views

app_name = 'login'
urlpatterns = [
    url(r'^$', views.UserFormView.as_view(), name='index'),
    url(r'^welcome/$', views.homepage, name='homepage'),
    url(r'^logout/$', views.logout_view, name='logout_user'),
    url(r'^registerPatient/$', views.PatientRegistrationView.as_view(), name='register_patient'),
    url(r'^registerDoctor/$', views.DoctorRegistrationView.as_view(), name='register_doctor'),
    url(r'^ajax/get_gps_for_hospital/$', utils.get_gps_for_hospital, name='get_gps_for_hospital'),
    url(r'^ajax/change_user_password/$', utils.change_user_password, name='change_user_password'),
]
