from django.contrib import admin

# Register your models here.
from login.models import Patient, Doctor

admin.site.register(Patient)
admin.site.register(Doctor)
