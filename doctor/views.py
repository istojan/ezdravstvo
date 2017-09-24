import datetime

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
from django.http import JsonResponse
from doctor.utils import get_apps_times_for_date


# from .forms import UserForm, PatientRegistrationForm, DoctorRegistrationForm
# from .utils import add_general_practitioner


@login_required(login_url='login:index')  # With this, if no user is logged in, than you will be redirected to the login page
def homepage(request, doctor_id):
    patient_count = 0
    context = {
        'patient_count': patient_count,
        'username': request.user.get_username(),
        'password': request.user.password,
        'doc_ID': request.user.doctor.doctor_id
    }

    if request.user.doctor.is_general_practitioner:
        return render(request, 'doctor/homepage_doctor_gp.html', context)

    return render(request, 'doctor/homepage_doctor_not_gp.html', context)


@login_required(login_url='login:index')  # With this, if no user is logged in, than you will be redirected to the login page
def get_times_available(request):
    year = request.GET.get('year', None)
    month = request.GET.get('month', None)
    day = request.GET.get('day', None)
    doctor = request.GET.get('doctor', None)

    list_all_times = get_apps_times_for_date()

    apps = Appointment.objects.filter(doctor__id=doctor).filter(date__day=day, date__month=month, date__year=year)
    print("There are " + str(len(apps)) + " apps on that date\n\n\n\n\n")

    for app in apps:
        print(app)
        print(app.doctor.id)
        print("App hour: " + str(app.time.hour))
        print("App min: " + str(app.time.minute))

    times_free_list = list()

    # Malce e shabanski, ama fuck it
    for time in list_all_times:
        tmp = time[1].split(':')    # parse hour and min from string object
        hour = int(tmp[0])
        min = int(tmp[1])

        time_available = True

        for app in apps:
            if int(app.time.hour) == hour and int(app.time.minute) == min:
                time_available = False
                break

        if time_available:
            times_free_list.append(time)

    data = {
        'times': times_free_list
    }
    return JsonResponse(data)


class MakeAppointmentView(View):
    form_class = AppointmentForm
    template_name = 'doctor/appointment.html'

    def get(self, request, doctor_id):
        # doctor_id can be removed from the url here
        form = self.form_class(doctor_id = request.user.doctor.doctor_id)

        return render(request, self.template_name, {'form': form})

    def post(self, request, doctor_id):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            print(form.cleaned_data.get('doctor').id)
            print(form.cleaned_data.get('patient'))
            date = str(form.cleaned_data.get('date2')).split(' ')[0]
            print(date)
            print(form.cleaned_data.get('time2'))
            appointment = Appointment(doctor=form.cleaned_data.get('doctor'),
                                      patient=form.cleaned_data.get('patient'),
                                      date=date,
                                      time=form.cleaned_data.get('time2'))
            appointment.save()
            print("App saved")
            return redirect('/doctor/' + str(request.user.id) + '/')
        else:
            print("Invalid form")

        return render(request, self.template_name, {'form': form})


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


class OldAppointmentsView(View):
    template_name = 'doctor/old_appointments.html'

    def get(self, request, doctor_id):
        doctor = Doctor.objects.get(user__pk=request.user.id)
        appointments = doctor.appointment_set.filter(date__lt=datetime.date.today())
        context = {
            'doctor': doctor,
            'appointments': appointments
        }
        return render(request, self.template_name, context)

    def post(self, request, doctor_id):
        pass


class UpcomingAppointmentsView(View):
    template_name = 'doctor/upcoming_appointments.html'

    def get(self, request, doctor_id):
        doctor = Doctor.objects.get(user__pk=request.user.id)
        appointments = doctor.appointment_set.exclude(date__lt=datetime.date.today())
        context = {
            'doctor': doctor,
            'appointments': appointments
        }
        return render(request, self.template_name, context)

    def post(self, request, doctor_id):
        pass


def remove_self_as_gp(request):
    patient_id = request.GET.get('patient_id', "")
    response = "Failure"
    if patient_id != "":
        try:
            patient = Patient.objects.get(pk=patient_id)
            if patient.general_practitioner_id == request.user.doctor.id:
                patient.general_practitioner = None
                patient.save()
                response = "Success"
        except Patient.DoesNotExist:
            response = "Failure"
    return JsonResponse({'response': response})


def add_self_as_gp(request):
    patient_id = request.GET.get('patient_id', "")
    response = "Failure"
    if patient_id != "":
        try:
            patient = Patient.objects.get(pk=patient_id)
            if patient.general_practitioner is None:
                doctor = request.user.doctor
                patient.general_practitioner = doctor
                patient.save()
                response = "Success"
        except Patient.DoesNotExist:
            response = "Failure"
    return JsonResponse({'response': response})


def patientDetails(request, doctor_id, patient_id):
    patient = Patient.objects.get(user__id=patient_id)
    doctors = Appointment.objects.filter(patient__user__id=patient_id)     # list of all doctors that the patinet had a appointment with

    past_appointments = Appointment.objects.filter(patient__user__id=patient_id).exclude(report=None)
    future_appointments = Appointment.objects.filter(patient__user__id=patient_id).filter(report=None)

    context = {
        'patient': patient,
        'past_appointments': past_appointments,
        'future_appointments': future_appointments
    }

    if patient.general_practitioner is None or patient.general_practitioner.user.id == int(doctor_id):
        return render(request, 'doctor/doctor_patient_details.html', context)
    else:
        for doctor in doctors:
            if doctor.user.id == int(doctor_id):
                return render(request, 'doctor/doctor_patient_details.html', context)

    return Http404("No patient like that")