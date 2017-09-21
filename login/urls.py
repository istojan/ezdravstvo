from django.conf.urls import url
from . import views

app_name = 'login'
urlpatterns = [
    url(r'^$', views.UserFormView.as_view(), name='index'),
    url(r'^welcome/$', views.homepage, name='homepage'),
    url(r'^logout/$', views.logout_view, name='logout_user'),
    url(r'^registerPatient/$', views.register_patient, name='register_patient'),
    url(r'^registerDoctor/$', views.register_doctor, name='register_doctor'),
]
