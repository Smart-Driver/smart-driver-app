# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-03 04:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('driver_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daystatement',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='ride',
            name='date',
            field=models.DateField(),
        ),
    ]
