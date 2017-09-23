

# Add a patient reference to a doctor (general practitioner)
from login.models import Doctor


def add_general_practitioner(patient, doctor_id):
    try:
        doctor = Doctor.objects.get(pk=doctor_id)
        print(doctor)
        patient.general_practitioner = doctor
        patient.save()
    except (ValueError, Doctor.DoesNotExist):
        pass


def add_hospital(doctor, hospital):
    doctor.hospital = hospital
    doctor.save()
