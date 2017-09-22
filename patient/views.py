from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from login.models import Patient, Doctor


def homepage(request, patient_id):
    # TODO Check patient_id == user_id
    patient = Patient.objects.get(user__pk=request.user.id)
    return render(request, 'patient/homepage.html', {'patient': patient})


def old_appointments(request, patient_id):
    return render(request, 'patient/old_appointments.html', {'patient_id': patient_id})


def upcoming_appointments(request, patient_id):
    return render(request, 'patient/upcoming_appointments.html', {'patient_id': patient_id})
