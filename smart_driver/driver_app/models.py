import json
import re
import requests
from django.db import models
from django.contrib.auth.models import User
# from decimal import *
# import dateutil.parser
# from dateutil.tz import *


class Ride(models.Model):
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE)
    week_statement = models.ForeignKey('WeekStatement', on_delete=models.CASCADE)
    day_statement = models.ForeignKey('DayStatement', on_delete=models.CASCADE)
    trip_id = models.CharField(max_length=50, primary_key=True)
    status = models.CharField(max_length=15)
    total_earned = models.DecimalField(max_digits=8, decimal_places=2)
    surge = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    distance = models.DecimalField(max_digits=7, decimal_places=2)
    date = models.DateTimeField()
    request_at = models.DateTimeField()
    begintrip_at = models.DateTimeField()
    dropoff_at = models.DateTimeField()
    duration = models.DurationField()


class DayStatement(models.Model):
    WEEKDAY_CHOICES = ((0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'),
                        (4, 'Friday'), (5, 'Suturday'), (6, 'Sunday'))
    total_rides = models.IntegerField(default=0)
    total_earned = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateTimeField()
    weekday = models.IntegerField(choices=WEEKDAY_CHOICES, default=0)
    time_worked = models.DurationField(null=True)
    rate_per_ride = models.DecimalField(max_digits=8, decimal_places=2)
    rate_per_hour = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    week_statement = models.ForeignKey('WeekStatement', on_delete=models.CASCADE)


class WeekStatement(models.Model):
    statement_id = models.CharField(max_length=50, primary_key=True)
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE)
    starting_at = models.DateTimeField()
    ending_at = models.DateTimeField()
    total_earned = models.DecimalField(max_digits=8, decimal_places=2)
    total_surge = models.DecimalField(max_digits=8, decimal_places=2)
    total_distance = models.DecimalField(max_digits=8, decimal_places=2, null=True)


class Driver(models.Model):
    u_user_id = models.CharField(max_length=50)
    email = models.EmailField()
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    @staticmethod
    def get_csrf_token(session):
        login_response = session.get('https://login.uber.com/login')
        csrf_token_pattern = '<input type="hidden" name="_csrf_token" value="([a-zA-Z0-9\_\-\=]+)">'
        csrf_token = re.search(csrf_token_pattern, login_response.text).group(1)
        return csrf_token

    @staticmethod
    def login(session, request):
        csrf_token = get_csrf_token(session)
        data = {
            'email': request.POST['email'],
            'password': request.POST['password'],
            '_csrf_token': csrf_token,
            'access_token': ''
        }
        login_response = session.post('https://login.uber.com/login', data)
        return login_response

    @staticmethod
    def get_statement_ids(login_response):
        cream_id_pattern = '"cream_invoice_uuid":"([a-zA-Z0-9\-]+)","'
        ids = re.findall(cream_id_pattern, login_response.text)
        return ids

    @staticmethod
    def get_statement(session, id):
        url = 'https://partners.uber.com/p3/money/statements/view/{}'.format(id)
        statement_response = session.get(url)
        data = json.loads(statement_response.text)
        return data
