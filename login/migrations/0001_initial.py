# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-20 14:21
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_number', models.IntegerField(unique=True)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('surname', models.CharField(max_length=30)),
                ('doctor_id', models.CharField(max_length=6)),
                ('is_general_practitioner', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('surname', models.CharField(max_length=30)),
                ('ssn', models.CharField(max_length=13, unique=True, validators=[django.core.validators.RegexValidator(code='nomatch', message='SSN must be 13 digits', regex='^[0-9]{13}$')])),
                ('email', models.EmailField(max_length=254)),
                ('date_of_birth', models.DateField()),
                ('address', models.CharField(max_length=30)),
                ('general_practitioner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='login.Doctor')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=10)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.Patient')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diagnosis', models.CharField(max_length=200)),
                ('therapy', models.CharField(max_length=200)),
                ('remark', models.CharField(max_length=300)),
                ('appointment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='login.Appointment')),
            ],
        ),
        migrations.CreateModel(
            name='Specialization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialization_name', models.CharField(max_length=20)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.Doctor')),
            ],
        ),
        migrations.AddField(
            model_name='doctor',
            name='hospital',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='login.Hospital'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointment',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='login.Doctor'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='login.Patient'),
        ),
    ]