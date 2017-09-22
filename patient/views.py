import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import Http404

# Create your views here.
from login.models import Patient, Doctor, Report


@login_required(login_url='login:index')
def homepage(request, patient_id):
    # TODO Check patient_id == user_id
    patient = Patient.objects.get(user__pk=request.user.id)
    return render(request, 'patient/homepage.html', {'patient': patient})


@login_required(login_url='login:index')
def old_appointments(request, patient_id):
    patient = Patient.objects.get(user__pk=request.user.id)
    appointments = patient.appointment_set.filter(date__lt=datetime.date.today())
    return render(request, 'patient/old_appointments.html', {'appointments': appointments,
                                                             'patient': patient})


@login_required(login_url='login:index')
def upcoming_appointments(request, patient_id):
    patient = Patient.objects.get(user__pk=request.user.id)
    appointments = patient.appointment_set.exclude(date__lt=datetime.date.today())
    return render(request, 'patient/upcoming_appointments.html', {'patient': patient,
                                                                  'appointments': appointments})


@login_required(login_url='login:index')
def appointment_details(request, report_id):
    try:
        report = Report.objects.get(pk=report_id)
        if report.appointment.patient.user_id == request.user.id:
            return render(request, 'patient/appointment_details.html', {'report': report})
        else:
            raise Http404("Извештајот не постои")
    except Report.DoesNotExist:
        raise Http404("Извештајот не постои")
