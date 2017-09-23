from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import SelectDateWidget

from login.models import Hospital


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  # the widget will hide the password from the user

    class Meta:
        model = User
        # fields = ['username', 'email', 'password']
        fields = ['email', 'password']
        # help_texts = {
        #     'username': None,
        #     'email': None,
        # }


# Choice fields which skips validation
class ChoiceFieldNoValidation(forms.ChoiceField):
    def validate(self, value):
        pass


class PatientRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=30)
    surname = forms.CharField(max_length=30)
    ssn = forms.CharField(min_length=13, max_length=13)
    date_of_birth = forms.DateField(widget=SelectDateWidget(years=range(1900, 2017)))
    address = forms.CharField(max_length=30)
    hospital = forms.ModelChoiceField(required=False,
                                      queryset=Hospital.objects.all(),
                                      widget=forms.Select(attrs={'onchange': 'get_doctors()'}))
    general_practitioner = ChoiceFieldNoValidation(required=False)

    class Meta:
        model = User
        fields = ('name', 'surname', 'ssn', 'date_of_birth', 'address', 'email', 'password1', 'password2',
                  'hospital', 'general_practitioner')


class DoctorRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=30)
    surname = forms.CharField(max_length=30)
    doctor_id = forms.CharField(max_length=6)
    hospital = forms.ModelChoiceField(queryset=Hospital.objects.all())
    is_general_practitioner = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ('name', 'surname', 'email', 'doctor_id', 'hospital', 'is_general_practitioner')
