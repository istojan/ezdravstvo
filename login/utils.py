# Add a patient reference to a doctor (general practitioner)
from django.contrib.auth.models import User
from django.http import JsonResponse

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


def get_gps_for_hospital(request):
    hospital_id = request.GET.get('hospital_id', "")
    data = []
    if hospital_id != "":
        doctors = Doctor.objects.filter(hospital__id=hospital_id, is_general_practitioner=True)
        for doctor in doctors:
            data.append({'id': doctor.id, 'name': "%s %s" % (doctor.name, doctor.surname)})
        print(data)
    return JsonResponse(data, safe=False)


def change_user_password(request):
    user_id = request.user.id
    old_password = request.POST['old_password']
    new_password = request.POST['new_password']
    confirm_password = request.POST['confirm_password']
    try:
        user = User.objects.get(pk=user_id)
        if not user.check_password(old_password):
            return JsonResponse({'error': 'Error changing password.'})
        if new_password != confirm_password:
            return JsonResponse({'error': 'Error changing password.'})
        user.set_password(new_password)
        user.save()
        return JsonResponse({'response': 'Successfully changed password.'})
    except User.DoesNotExist:
        return JsonResponse({'error': 'Error changing password.'})