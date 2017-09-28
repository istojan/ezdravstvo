from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect, JsonResponse
# from .forms import UserLoginForm
from django.views.generic import View
from django.contrib.auth.decorators import login_required

from login.models import Patient, Doctor
from .forms import UserForm, PatientRegistrationForm, DoctorRegistrationForm
from .utils import add_general_practitioner, add_hospital


class UserFormView(View):
    form_class = UserForm
    template_name = 'login/index.html'

    # display a blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']

        print(email)
        print(password)

        # returns User objects if credentials are correct
        user = authenticate(request, email=email, password=password)

        if user is not None:
            print("User is authenticated")
            if user.is_active:
                print("User is active")
                # to log in a user
                login(request, user)
                print("User is logged in atm")
                # , {'username', request.user.get_username()}
                return redirect('login:homepage')  # redirect to home page

        return render(request, self.template_name, {'form': UserForm(None)})


@login_required(login_url='login:index')  # With this, if no user is logged in, than you will be redirected to the login page
def homepage(request):
    print("Trying to return homepage to user")

    if request.user.is_authenticated():
        print("User has been already authenticated")

        try:
            if request.user.doctor:    # This will throw an error if its a doctor
                print("This is a doctor")

            # return homepage for doctor
            return redirect('doctor:homepage_doc', doctor_id=request.user.id)

        except Exception as e:
            # return homepage for patient
            return redirect('patient:homepage', patient_id=request.user.id)

    else:
        print("User has not been authenticated")
        return HttpResponseRedirect(reverse('login:index'))  # request to default page if no user is logged in


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login:index'))


class PatientRegistrationView(View):
    form_class = PatientRegistrationForm
    template_name = 'login/register_patient.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        print('Method = POST')

        if form.is_valid():
            print("Valid form")
            user = form.save()
            user.refresh_from_db()
            user.patient = Patient(name=form.cleaned_data.get('name'),
                                   surname=form.cleaned_data.get('surname'),
                                   ssn=form.cleaned_data.get('ssn'),
                                   date_of_birth=form.cleaned_data.get('date_of_birth'),
                                   address=form.cleaned_data.get('address'))
            user._type = 'P'  # Tip na user
            user.save()
            gp = form.cleaned_data.get('general_practitioner')
            add_general_practitioner(user.patient, gp)
            print("User saved")
            user = authenticate(request, email=request.POST['email'], password=request.POST['password1'])
            print("User authenticated")
            login(request, user)
            print("User logged in")

            return redirect('login:homepage')

        print("Invalid form")
        return render(request, self.template_name, {'form': form})


class DoctorRegistrationView(View):
    form_class = DoctorRegistrationForm
    template_name = 'login/register_doctor.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        print('Method = POST')

        if form.is_valid():
            print("Valid form")
            user = form.save()
            user.refresh_from_db()

            user.doctor = Doctor(name=form.cleaned_data.get('name'), surname=form.cleaned_data.get('surname'),
                                 doctor_id=form.cleaned_data.get('doctor_id'),
                                 is_general_practitioner=form.cleaned_data.get('is_general_practitioner'))
            user._type = 'D'  # Tip na user
            user.save()
            hospital = form.cleaned_data.get('hospital')
            add_hospital(user.doctor, hospital)
            print("User saved")
            user = authenticate(request, email=request.POST['email'], password=request.POST['password1'])
            print("User authenticated")
            login(request, user)
            print("User logged in")
            return redirect('login:homepage')

        print("Invalid form")
        return render(request, self.template_name, {'form': form})

# # View for patient registration
# def register_patient(request):
#     if request.method == 'POST':
#         form = PatientRegistrationForm(request.POST)
#         print('Method = POST')
#         if form.is_valid():
#             print("Valid form")
#             user = form.save()
#             user.refresh_from_db()
#             user.patient = Patient()
#             user.patient.name = form.cleaned_data.get('name')
#             user.patient.surname = form.cleaned_data.get('surname')
#             user.patient.ssn = form.cleaned_data.get('ssn')
#             user.patient.date_of_birth = form.cleaned_data.get('date_of_birth')
#             print(" Date of birth: ", form.cleaned_data.get('date_of_birth'))
#             user.patient.address = form.cleaned_data.get('address')
#             user.patient.email = form.cleaned_data.get('email')
#             user._type = 'P'  # Tip na user
#             user.save()
#             gp = form.cleaned_data.get('general_practitioner')
#             add_general_practitioner(user.patient, gp)
#             print("User saved")
#             user = authenticate(request, email=request.POST['email'], password=request.POST['password1'])
#             print("User authenticated")
#             login(request, user)
#             print("User logged in")
#             return redirect('login:homepage')
#         else:
#             print("Invalid form")
#     else:
#         print("Method = GET")
#         form = PatientRegistrationForm()
#     return render(request, 'login/register_patient.html', {'form': form})
#
#
# # View for doctor registration
# def register_doctor(request):
#     if request.method == 'POST':
#         form = DoctorRegistrationForm(request.POST)
#         print("Method = POST")
#         if form.is_valid():
#             print("Valid form")
#             user = form.save()
#             user.refresh_from_db()
#             name = form.cleaned_data.get('name')
#             surname = form.cleaned_data.get('surname')
#             doctor_id = form.cleaned_data.get('doctor_id')
#             is_general_practitioner = form.cleaned_data.get('is_general_practitioner')
#             user.doctor = Doctor(name=name, surname=surname, doctor_id=doctor_id,
#                                  is_general_practitioner=is_general_practitioner)
#             user._type = 'D'  # Tip na user
#             user.save()
#             print("User saved")
#             user = authenticate(request, email=request.POST['email'], password=request.POST['password1'])
#             print("User authenticated")
#             login(request, user)
#             print("User logged in")
#             return redirect('login:homepage')
#         else:
#             print("Method = GET")
#     else:
#         form = DoctorRegistrationForm()
#     return render(request, 'login/register_doctor.html', {'form': form})
