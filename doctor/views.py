from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect, Http404
# from .forms import UserLoginForm
from django.views.generic import View
from django.contrib.auth.decorators import login_required

from login.models import Patient, Doctor, Appointment
from doctor.forms import AppointmentForm

# from .forms import UserForm, PatientRegistrationForm, DoctorRegistrationForm
# from .utils import add_general_practitioner


@login_required(login_url='login:index')  # With this, if no user is logged in, than you will be redirected to the login page
def homepage(request, doctor_id):
    # print("\n\n\n We are now in doctor homepage view \n\n\n")

    # need to do a patient count for the specific doctor
    patient_count = 0

    # patients = Patient.objects.filter(doctor__doctor)
    # appointments = Appointment.objects.get
    # appointments = Appointment.objects.filter(doctor__doctor_id=doctor_id).filter(date < datetime.date.today())


    context = {
        'patient_count': patient_count,
        'username': request.user.get_username(),
        'password': request.user.password,
        'doc_ID': request.user.doctor.doctor_id
    }

    return render(request, 'doctor/homepage_doctor.html', context)


class MakeAppointmentView(View):
    form_class = AppointmentForm
    template_name = 'doctor/appointment.html'

    def get(self, request, doctor_id):
        # doctor_id can be removed from the url here

        # context = {
        #     'doctor_id': request.user.doctor.doctor_id
        # }
        form = self.form_class(request.user.doctor.doctor_id)

        return render(request, self.template_name, {'form': form})

    def post(self, request):
        pass


class PatientsPreviewView(View):
    template_name = 'doctor/patients_preview.html'

    def get(self, request, doctor_id):
        doctor = Doctor.objects.get(user__pk=request.user.id)
        if not doctor.is_general_practitioner:
            raise Http404("Не сте матичен доктор!") # TODO Drug view za nematichni doktori
        doctors_patients = doctor.patient_set.all()
        patients_without_gp = Patient.objects.filter(general_practitioner=None)
        context = {
            'doctor': doctor,
            'doctors_patients': doctors_patients,
            'patients_without_gp': patients_without_gp
        }
        return render(request, self.template_name, context)

    def post(self, request, doctor_id):
        pass
