# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-29 21:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0007_auto_20170929_2337'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='has_report_added',
            field=models.BooleanField(default=False),
        ),
    ]
