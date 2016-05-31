from django.db import models
# from decimal import *
# import dateutil.parser
# from dateutil.tz import *


class Ride(models.Model):
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE)
    week_statement = models.ForeignKey('WeekStatement', on_delete=models.CASCADE)
    day_statement = models.ForeignKey('DayStatement', on_delete=models.CASCADE)
    trip_id = models.CharField(max_length=50, primary_key=True)
    status = models.CharField(max_length=15)
    fare = models.DecimalField(max_digits=8, decimal_places=2)
    uber_fee = models.DecimalField(max_digits=7, decimal_places=2)
    total_earned = models.DecimalField(max_digits=8, decimal_places=2)
    surge = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    currency_code = models.CharField(max_length=5)
    distance = models.DecimalField(max_digits=7, decimal_places=2)
    date = models.DateTimeField()
    request_at = models.DateTimeField()
    begintrip_at = models.DateTimeField()
    dropoff_at = models.DateTimeField()
    duration = models.DurationField()
    driver_feedback = models.PositiveSmallIntegerField()
    driver_rating = models.DecimalField(max_digits=3, decimal_places=2)
    ride_type = models.CharField(max_length=25)


class DayStatement(models.Model):
    WEEKDAY_CHOICES = ((0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'),
                        (4, 'Friday'), (5, 'Suturday'), (6, 'Sunday'))
    total_rides = models.IntegerField(default=0)
    total_earned = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateTimeField()
    weekday = models.IntegerField(choices=WEEKDAY_CHOICES, default=0)
    time_worked = models.DurationField()
    rate_per_ride = models.DecimalField(max_digits=8, decimal_places=2)
    rate_per_hour = models.DecimalField(max_digits=8, decimal_places=2)
    week_statement = models.ForeignKey('WeekStatement', on_delete=models.CASCADE)


class WeekStatement(models.Model):
    statement_id = models.CharField(max_length=50, primary_key=True)
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE)
    starting_at = models.DateTimeField()
    ending_at = models.DateTimeField()
    total_earned = models.DecimalField(max_digits=8, decimal_places=2)
    total_fare = models.DecimalField(max_digits=8, decimal_places=2)
    total_uber_fee = models.DecimalField(max_digits=8, decimal_places=2)
    total_surge = models.DecimalField(max_digits=8, decimal_places=2)
    trip_count = models.PositiveSmallIntegerField()
    total_distance = models.DecimalField(max_digits=8, decimal_places=2)
    city = models.SlugField(max_length=100)


class Driver(models.Model):
    u_user_id = models.CharField(max_length=50)
    email = models.EmailField()
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
