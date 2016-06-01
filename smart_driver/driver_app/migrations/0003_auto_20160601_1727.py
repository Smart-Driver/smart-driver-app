# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-01 17:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('driver_app', '0002_auto_20160531_2105'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ride',
            name='currency_code',
        ),
        migrations.RemoveField(
            model_name='ride',
            name='driver_feedback',
        ),
        migrations.RemoveField(
            model_name='ride',
            name='driver_rating',
        ),
        migrations.RemoveField(
            model_name='ride',
            name='fare',
        ),
        migrations.RemoveField(
            model_name='ride',
            name='ride_type',
        ),
        migrations.RemoveField(
            model_name='ride',
            name='uber_fee',
        ),
        migrations.RemoveField(
            model_name='weekstatement',
            name='city',
        ),
        migrations.RemoveField(
            model_name='weekstatement',
            name='total_fare',
        ),
        migrations.RemoveField(
            model_name='weekstatement',
            name='total_uber_fee',
        ),
        migrations.RemoveField(
            model_name='weekstatement',
            name='trip_count',
        ),
        migrations.AlterField(
            model_name='daystatement',
            name='rate_per_hour',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='daystatement',
            name='time_worked',
            field=models.DurationField(null=True),
        ),
        migrations.AlterField(
            model_name='weekstatement',
            name='total_distance',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
    ]