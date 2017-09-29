from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render

# Create your views here.
from login.models import Patient, Report, Appointment


@login_required(login_url='login:index')
def homepage(request, patient_id):
    # TODO Check patient_id == user_id
    patient = Patient.objects.get(user__pk=request.user.id)
    old_appointments1 = patient.appointment_set.exclude(has_report_added=False)
    upcoming_appointments1 = patient.appointment_set.filter(has_report_added=False)
    return render(request, 'patient/homepage.html', {
        'patient': patient,
        'old_appointments': old_appointments1,
        'upcoming_appointments': upcoming_appointments1
    })


@login_required(login_url='login:index')
def old_appointments(request, patient_id):
    patient = Patient.objects.get(user__pk=request.user.id)
    appointments = patient.appointment_set.exclude(has_report_added=False)
    return render(request, 'patient/old_appointments.html', {'appointments': appointments,
                                                             'patient': patient})


@login_required(login_url='login:index')
def upcoming_appointments(request, patient_id):
    patient = Patient.objects.get(user__pk=request.user.id)
    appointments = patient.appointment_set.filter(has_report_added=False)
    return render(request, 'patient/upcoming_appointments.html', {'patient': patient,
                                                                  'appointments': appointments})


@login_required(login_url='login:index')
def appointment_details(request, patient_id, appointment_id):
    try:
        appointment = Appointment.objects.get(pk=appointment_id)
        if appointment.patient.user.id == request.user.id:
            return render(request, 'patient/appointment_details.html', {'appointment': appointment})
        else:
            raise Http404("Извештајот не постои")
    except Report.DoesNotExist:
        raise Http404("Извештајот не постои")
