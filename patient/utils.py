from django.http import JsonResponse

from login.models import Patient


def get_patient_personal_info(request):
    patient_id = request.GET.get('patient_id', "")
    response = "Грешка при вчитување на податоците."
    if patient_id != "":
        try:
            patient = Patient.objects.get(id=patient_id)
            response = {
                'name': patient.name,
                'surname': patient.surname,
                'ssn': patient.ssn,
                'date_of_birth': patient.date_of_birth,
                'address': patient.address,
                'email': patient.user.email,
                'gp': patient.general_practitioner.__str__()
            }
            return JsonResponse(response)
        except Patient.DoesNotExist:
            response = "Грешка при вчитување на податоците."
            return JsonResponse({'error': response})
    else:
        return JsonResponse({'error': response})


def get_old_appointments(request):
    patient_id = request.GET.get('patient_id', "")
    response = "Грешка при вчитување на податоците."
    if patient_id != "":
        try:
            patient = Patient.objects.get(id=patient_id)
            appointments = patient.appointment_set.exclude(report=None)
            response = []
            for appointment in appointments:
                response.append({
                    'app_id': appointment.id,
                    'patient_id': appointment.patient.id,
                    'number': appointment.appointment_number,
                    'doctor': appointment.doctor.__str__(),
                    'date': appointment.date,
                    'time': appointment.time
                })
            return JsonResponse(response, safe=False)
        except Patient.DoesNotExist:
            response = "Грешка при вчитување на податоците."
            return JsonResponse({'error': response})
    else:
        return JsonResponse({'error': response})


def get_upcoming_appointments(request):
    patient_id = request.GET.get('patient_id', "")
    response = "Грешка при вчитување на податоците."
    if patient_id != "":
        try:
            patient = Patient.objects.get(id=patient_id)
            appointments = patient.appointment_set.filter(report=None)
            response = []
            for appointment in appointments:
                response.append({
                    'number': appointment.appointment_number,
                    'doctor': appointment.doctor.__str__(),
                    'date': appointment.date,
                    'time': appointment.time
                })
            return JsonResponse(response, safe=False)
        except Patient.DoesNotExist:
            response = "Грешка при вчитување на податоците."
            return JsonResponse({'error': response})
    else:
        return JsonResponse({'error': response})