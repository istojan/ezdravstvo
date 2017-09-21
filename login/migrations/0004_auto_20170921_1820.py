# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-21 16:20
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_auto_20170921_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='date_of_birth',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='patient',
            name='ssn',
            field=models.CharField(max_length=13, validators=[django.core.validators.RegexValidator(code='nomatch', message='SSN must be 13 digits', regex='^[0-9]{13}$')]),
        ),
    ]