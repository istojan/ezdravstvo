from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import SelectDateWidget

from login.models import Doctor, Patient, Appointment
from doctor.utils import get_list_dates, get_apps_times_for_date
import datetime


class AppointmentForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(label="Доктор", required=True, queryset=Doctor.objects.filter(is_general_practitioner=False))
    # patient = forms.ModelChoiceField(required=True, queryset=Patient.objects.filter(general_practitioner__doctor_id=data.doctor_id))
    # date = forms.DateField(label="Датум", widget=SelectDateWidget(years=range(1900, 2017)))
    # time = forms.TimeField(label="Време", widget=forms.TimeInput(format='%H:%M'))
    date2 = forms.ChoiceField()
    time2 = forms.ChoiceField()

    def __init__(self, doctor_id, *args, **kwargs):  # we give the id of the doctor that will make the appointment. He can make appointments for only his patients
        self.doctor_id = doctor_id
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields['patient'] = forms.ModelChoiceField(label="Пациент", required=True, queryset=Patient.objects.filter(general_practitioner__doctor_id=self.doctor_id))

        choices_dates = get_list_dates(14)
        # choices_times = get_apps_times_for_date()

        self.fields['date2'] = forms.ChoiceField(
            label="Датум",
            choices=choices_dates,
            widget=forms.Select(attrs={'onchange': 'make_change()'})
        )

        queryset = Doctor.objects.filter(is_general_practitioner=False)

        for q in queryset:
            print(q)
            print("  doc_id =  " +  str(q.doctor_id) + "   doc_pk = " + str(q.id))

        queryset = Patient.objects.filter(general_practitioner__doctor_id=self.doctor_id)

        for q in queryset:
            print(q)
            print("  patient_pk = " + str(q.id))

        # self.fields['time2'] = forms.ChoiceField(
        #     label="Термин",
        #     choices=choices_times
        # )

    class Meta:
        model = Appointment
        fields = [
            'doctor', 'patient','date2', 'time2'
        ]
        # labels = {
        #     "doctor": "Доктор",
        #     "patient": "Пациент",
        #     "time": "Време",
        #     "date": "Датум"
        # }

    # class ChangeEmailForm(forms.ModelForm):
    #     def __init__(self, user, *args, **kwargs):
    #         self.user = user
    #         super(ChangeEmailForm, self).__init__(*args, **kwargs)
    #         self.fields['email'].initial = user.email
    #
    #     class Meta:
    #         model = User
    #         fields = ('email',)
    #
    #     def save(self, commit=True):
    #         self.user.email = self.cleaned_data['email']
    #         if commit:
    #             self.user.save()
    #         return self.user


# class UserForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)  # the widget will hide the password from the user
#
#
#     class Meta:
#         model = User
#         # fields = ['username', 'email', 'password']
#         fields = ['email', 'password']
#         # help_texts = {
#         #     'username': None,
#         #     'email': None,
#         # }
#
#
# class PatientRegistrationForm(UserCreationForm):
#     name = forms.CharField(max_length=30)
#     surname = forms.CharField(max_length=30)
#     ssn = forms.CharField(min_length=13, max_length=13)
#     date_of_birth = forms.DateField(widget=SelectDateWidget(years=range(1900, 2017)))
#     address = forms.CharField(max_length=30)
#     email = forms.EmailField()
#     general_practitioner = forms.ModelChoiceField(required=False,
#                                                   queryset=Doctor.objects.filter(is_general_practitioner=True))
#
#     class Meta:
#         model = User
#         fields = ('name', 'surname', 'ssn', 'date_of_birth', 'address', 'email', 'password1', 'password2',
#                   'general_practitioner')
#
#
# class DoctorRegistrationForm(UserCreationForm):
#     name = forms.CharField(max_length=30)
#     surname = forms.CharField(max_length=30)
#     doctor_id = forms.CharField(max_length=6)
#     is_general_practitioner = forms.BooleanField(required=False)
#
#     class Meta:
#         model = User
#         fields = ('name', 'surname', 'email', 'doctor_id', 'is_general_practitioner')
