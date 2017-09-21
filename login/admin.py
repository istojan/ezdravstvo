from django.contrib import admin
# from django.contrib.auth.models import User

# Register your models here.
from login.models import Patient, Doctor

admin.site.register(Patient)
admin.site.register(Doctor)
# admin.site.register(User)
