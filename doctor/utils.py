import datetime

# returns a list of pairs of datetime and string of datetime suitable to be given as an argument od ChoiceFields.choices
# List contains only weekdays
from django.http import JsonResponse

from login.models import Doctor, Appointment, Patient


def get_list_dates(count_days):
    d = datetime.datetime.now()
    delta = datetime.timedelta(days=1)
    end_date = d + count_days * delta

    print("Now: ", d)
    print("End date: ", end_date)

    choices_dates = list()

    while d <= end_date:
        if d.weekday() < 5:
            choices_dates.append((d, d.strftime("%Y-%m-%d")))
        d += delta

    return choices_dates


def get_apps_times_for_date():
    # find a way to use date

    d = datetime.datetime(2014, 5, 12, 8,
                          00)  # first 3 numbers don't matter, I only use hours and minutes from this temporary object
    delta = datetime.timedelta(minutes=20)
    choices_times = list()

    while d.hour < 16:
        choices_times.append((d.strftime('%H:%M'), d.strftime('%H:%M')))
        d += delta

    return choices_times


def get_doctors_for_hospital(request):
    hospital_id = request.GET.get('hospital_id', "")
    data = []
    if hospital_id != "":
        if hospital_id != "all":
            doctors = Doctor.objects.filter(hospital__id=hospital_id, is_general_practitioner=False)
        else:
            doctors = Doctor.objects.filter(is_general_practitioner=False)
        for doctor in doctors:
            data.append({'id': doctor.id, 'name': "%s %s" % (doctor.name, doctor.surname)})
        print(data)
    return JsonResponse(data, safe=False)


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


def remove_report_from_appointment(request):
    appointment_id = request.GET.get('appointment_id', "")
    response = "Failure"
    if appointment_id != "":
        try:
            appointment = Appointment.objects.get(pk=appointment_id)
            appointment.report.delete()
            appointment.save()
            response = "Success"
        except Appointment.DoesNotExist:
            response = "Failure"
    return JsonResponse({'response': response})

def get_patients_list(request):
    doctor = request.user.doctor
    print(doctor.id)
    data = []
    # doctor = Doctor.objects.get(user__pk=request.user.id)
    if not doctor.is_general_practitioner:
        apps = Appointment.objects.filter(doctor__user__id=request.user.id).filter(has_report_added=True)
        patients = set()
        for app in apps:
            patients.add(app.patient)
        # data.append({'patients': patients})
        print("Returning patients")
        total = 0
        for patient in patients:
            total += 1
            data.append({'name': patient.name, 'surname': patient.surname, 'email': patient.user.email, 'patient_id': patient.user.id})
        return JsonResponse({'total': total, 'patients': data})
    else:
        doctors_patients = doctor.patient_set.all()
        patients_without_gp = Patient.objects.filter(general_practitioner=None)
        context = {
            'doctors_patients': doctors_patients,
            'patients_without_gp': patients_without_gp
        }



    return JsonResponse({'response': context})


def get_appointments_list(request):
    doctor = request.user.doctor
    print(doctor.id)
    data = []
    # doctor = Doctor.objects.get(user__pk=request.user.id)
    if not doctor.is_general_practitioner:
        apps = Appointment.objects.filter(doctor__user__id=request.user.id).filter(has_report_added=False)

        total = 0

        for app in apps:
            total += 1
            data.append({'app_num': app.appointment_number, 'app_id': app.id, 'patient_name': app.patient.__str__(),
                         'date': app.date, 'time': app.time})
        # data.append({'patients': patients})
        print("Returning apps")

        return JsonResponse({'total': total, 'apps': data})
    else:
        doctors_patients = doctor.patient_set.all()
        patients_without_gp = Patient.objects.filter(general_practitioner=None)
        context = {
            'doctors_patients': doctors_patients,
            'patients_without_gp': patients_without_gp
        }

    return JsonResponse({'response': context})