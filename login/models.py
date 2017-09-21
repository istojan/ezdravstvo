from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

# TODO - Referencijalniot integritet - Shto da se brishe i kako da se odnesuvaat redovite pri brishenje


# ZDRAVSTVENA INSTITUCIJA
#
# - ime
# - adresa
from django.db.models.signals import post_save


class Hospital(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=30)


# DOKTOR
#
# user -> referenca kon User (nasleduvanje)
# ime
# prezime
# doktorska identifikacija
# dali e matichen doktor
# hospital -> referenca kon Hospital (zdravstvena institucija kaj shto raboti)
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    doctor_id = models.CharField(max_length=6)
    # Dali e matichen doktor
    is_general_practitioner = models.BooleanField(default=False)
    hospital = models.ForeignKey(Hospital, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "Dr. %s %s" % (self.name, self.surname)


# PACIENT
#
# user -> referenca kon User (nsleduvanje)
# ime
# prezime
# matichen broj
# email
# data na ragjanje
# general_practitioner -> referenca kon Doctor (matichen)
# TODO Kako da gi realizirame vakcinite?
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    ssn = models.CharField(max_length=13, validators=[
        RegexValidator(regex='^[0-9]{13}$', message='SSN must be 13 digits', code='nomatch')
    ])
    # email = models.EmailField(null=True, default=None)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=30)
    # Matichen doktor
    general_practitioner = models.ForeignKey(Doctor, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "%s %s" % (self.name, self.surname)


# TELEFONSKI BROJ
#
# patient -> referenca kon Patient (sopstvenik na telefonot)
# telefonskiot broj
class PhoneNumber(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    number = models.CharField(max_length=10)


# DOKTORSKA SPECIJALIZACIJA
#
# doctor -> referenca kon Doctor (na koj doktor se odnesuva spicijalizacijata)
# spicijalizacijata
class Specialization(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    specialization_name = models.CharField(max_length=20)


# PREGLED / TERMIN
#
# br. na pregled
# patient -> referenca kon Patient (pacient za kogo e pregledot)
# doctor -> referenca kon Doctor (doktor koj go izvrshuva pregledot)
# datum
# chas
class Appointment(models.Model):
    appointment_number = models.IntegerField(unique=True)
    patient = models.ForeignKey(Patient, on_delete=models.DO_NOTHING)
    doctor = models.ForeignKey(Doctor, on_delete=models.DO_NOTHING)
    date = models.DateField()
    time = models.TimeField()
    # Verojatno e podobro da bide so DateTimeFiled
    # date_time = models.DateTimeField()


# IZVESHTAJ
#
# appointment -> referenca kon Appointment (za koj pregled e izveshtajot)
# dijagnoza
# terapija
# zabeleshka
class Report(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    diagnosis = models.CharField(max_length=200)
    therapy = models.CharField(max_length=200)
    remark = models.CharField(max_length=300)


def create_profile(sender, **kwargs):
    print("Creating profile")
    user = kwargs['instance']
    if user.is_superuser:
        return
    if kwargs['created']:
        print("created == True")
        if hasattr(user, '_type'):
            print("Has _type")
            if user._type == 'P':
                patient = Patient(user=user)
                patient.save()
                print("Saving patient")
            elif user._type == 'D':
                doctor = Doctor(user=user)
                doctor.save()
                print("Saving doctor")
    if hasattr(user, '_type'):
        if user._type == 'P':
            user.patient.save()
            print("Saving user.patient")
        elif user._type == 'D':
            user.doctor.save()
            print("Saving user.doctor")


post_save.connect(create_profile, sender=User)
