import datetime

# returns a list of pairs of datetime and string of datetime suitable to be given as an argument od ChoiceFields.choices
# List contains only weekdays
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from login.models import Doctor, Appointment, Patient, Report


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


@login_required(login_url='login:index')
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


@login_required(login_url='login:index')
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


@login_required(login_url='login:index')
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


@login_required(login_url='login:index')
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


@login_required(login_url='login:index')
def get_patients_list(request):
    doctor = request.user.doctor

    if not doctor.is_general_practitioner:
        apps = Appointment.objects.filter(doctor__user__id=request.user.id).filter(has_report_added=True)
        patients = set()
        for app in apps:
            patients.add(app.patient)

        print("Returning patients")
        data, total = get_string_list_patients(patients)

        return JsonResponse({'total': total, 'patients': data})
    else:
        doctors_patients = doctor.patient_set.all()
        patients_without_gp = Patient.objects.filter(general_practitioner=None)

        data_doctor_patients, total_doctor_patients = get_string_list_patients(doctors_patients)
        data_no_gp_patients, total_no_gp_patients = get_string_list_patients(patients_without_gp)

        return JsonResponse({'total_gp': total_doctor_patients, 'patients_gp': data_doctor_patients, 'total_no_gp': total_no_gp_patients, 'patients_no_gp': data_no_gp_patients})


def get_string_list_patients(patients):
    data = []
    total = 0
    for patient in patients:
        total += 1
        data.append({'name': patient.name, 'surname': patient.surname, 'email': patient.user.email,
                     'patient_id': patient.user.id, 'ssn': patient.ssn})
    return data, total


@login_required(login_url='login:index')
def get_appointments_list(request):
    doctor = request.user.doctor

    if not doctor.is_general_practitioner:
        apps = Appointment.objects.filter(doctor__user__id=request.user.id).filter(has_report_added=False)
        total, data = get_string_list_apps(apps)
    else:
        apps = Appointment.objects.filter(doctor__user__id=request.user.id).filter(has_report_added=True)
        total, data = get_string_list_apps(apps)

    return JsonResponse({'total': total, 'apps': data})


def get_string_list_apps(apps):
    total = 0
    data = []

    for app in apps:
        total += 1
        data.append({'app_num': app.appointment_number, 'app_id': app.id, 'patient_name': app.patient.__str__(),
                     'date': app.date, 'time': app.time, 'ssn': app.patient.ssn})

    return total, data


@login_required(login_url='login:index')
def get_patient_apps_list(request):
    patient_email = request.GET['patient_email']

    apps_past = Appointment.objects.all().filter(patient__user__email=patient_email).filter(has_report_added=True)
    apps_future = Appointment.objects.all().filter(patient__user__email=patient_email).filter(has_report_added=False)

    total_past, apps_past_string = get_string_list_apps(apps_past)
    total_future, apps_future_string = get_string_list_apps(apps_future)

    return JsonResponse({'total_past': total_past, 'apps_past': apps_past_string, 'total_future': total_future, 'apps_future': apps_future_string})


@login_required(login_url='login:index')
def add_gp_appointment(request):
    doctor_id = request.POST['doctor_id']
    patient_id = request.POST['patient_id']
    diagnosis = request.POST['diagnosis']
    therapy = request.POST['therapy']
    remark = request.POST['remark']
    try:
        doctor = Doctor.objects.get(pk=doctor_id)
        patient = Patient.objects.get(pk=patient_id)
        app = Appointment(patient=patient, doctor=doctor, date=datetime.date.today(), time='00:00', has_report_added=True)
        app.save()
        report = Report(appointment=app, diagnosis=diagnosis, therapy=therapy, remark=remark)
        report.save()
        return JsonResponse({'success': ""})
    except (Doctor.DoesNotExist, Patient.DoesNotExist):
        return JsonResponse({'error': 'Грешка при внесување на прегледот!'})
