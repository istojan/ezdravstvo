from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
# from .forms import UserLoginForm
from django.views.generic import View
from django.contrib.auth.decorators import login_required

from login.models import Patient, Doctor, Appointment
from doctor.forms import AppointmentForm
from django.http import JsonResponse


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


@login_required(login_url='login:index')  # With this, if no user is logged in, than you will be redirected to the login page
def get_times_available(request):
    year = request.GET.get('year', None)
    month = request.GET.get('month', None)
    day = request.GET.get('day', None)
    doctor = request.GET.get('doctor', None)
    # patient = request.GET.get('year', None)
    print("Year " + year)
    print("Doctor " + doctor)

    data = {
        'is_taken': True
    }
    return JsonResponse(data)

    # return render(request, 'doctor/homepage_doctor.html')



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