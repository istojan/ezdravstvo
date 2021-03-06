from django import forms

from login.models import Doctor, Patient, Appointment, Report, Hospital
from doctor.utils import get_list_dates
from login.forms import ChoiceFieldNoValidation


class AppointmentForm(forms.ModelForm):
    hospital = forms.ModelChoiceField(label="Здравствена установа", required=False,
                                      queryset=Hospital.objects.all(),
                                      widget=forms.Select(attrs={'onchange': 'get_doctors_for_hospital()'}))
    doctor = forms.ModelChoiceField(label="Доктор", required=True,
                                    queryset=Doctor.objects.filter(is_general_practitioner=False))
    date2 = ChoiceFieldNoValidation()
    time2 = ChoiceFieldNoValidation(label='Време')

    def __init__(self, *args, **kwargs):  # we give the id of the doctor that will make the appointment. He can make appointments for only his patients
        if 'doctor_id' not in kwargs:
            super(AppointmentForm, self).__init__(*args, **kwargs)
            return

        self.doctor_id = kwargs.pop('doctor_id')
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields['patient'] = forms.ModelChoiceField(label="Пациент", required=True, queryset=Patient.objects.filter(
                            general_practitioner__doctor_id=self.doctor_id))

        # self.doctor_id = doctor_id
        # self.fields['patient'] = ChoiceFieldNoValidation(label="Пациент", required=True, choices=Patient.objects.filter(general_practitioner__doctor_id=self.doctor_id))

        choices_dates = get_list_dates(14)
        blank_choice = ('', '---------')
        choices_dates.insert(0, blank_choice)

        self.fields['date2'] = ChoiceFieldNoValidation(
            label="Датум",
            choices=choices_dates,
            required=True,
            widget=forms.Select(attrs={'onchange': 'make_change()'})
        )

    class Meta:
        model = Appointment
        fields = [
            'hospital', 'doctor', 'patient', 'date2', 'time2'
        ]


class AddReportForm(forms.ModelForm):
    therapy = forms.CharField(label="Терапија", max_length=200, required=False)
    remark = forms.CharField(label="Забелешка", max_length=200, required=False)

    class Meta:
        model = Report
        fields = ['diagnosis', 'therapy', 'remark']
        labels = {
            'diagnosis': 'Дијагноза'
        }
