from django.contrib import admin

# Register your models here.
from login.models import Appointment, Report

admin.site.register(Appointment)
admin.site.register(Report)
