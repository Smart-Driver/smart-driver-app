import json
import re
import requests
import datetime
import dateutil.parser
from dateutil.tz import *
from decimal import *
from django.db import models
from django.db.models import Min, Max, Sum, Avg
from django.contrib.auth.models import User

class Ride(models.Model):
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE)
    week_statement = models.ForeignKey('WeekStatement', on_delete=models.CASCADE)
    day_statement = models.ForeignKey('DayStatement', on_delete=models.CASCADE)
    month_statement = models.ForeignKey('MonthStatement', on_delete=models.CASCADE, null=True)
    trip_id = models.CharField(max_length=50, primary_key=True)
    status = models.CharField(max_length=15)
    total_earned = models.DecimalField(max_digits=8, decimal_places=2)
    surge = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    distance = models.DecimalField(max_digits=7, decimal_places=2)
    date = models.DateField()
    request_at = models.DateTimeField()
    begintrip_at = models.DateTimeField(null=True)
    dropoff_at = models.DateTimeField(null=True)
    duration = models.DurationField()


class DayStatement(models.Model):
    WEEKDAY_CHOICES = ((0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'),
                        (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday'))
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE)
    total_rides = models.IntegerField(default=0, null=True)
    total_earned = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    date = models.DateField()
    weekday = models.IntegerField(choices=WEEKDAY_CHOICES, default=0)
    time_worked = models.DurationField(null=True)
    rate_per_ride = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    rate_per_hour = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    week_statement = models.ForeignKey('WeekStatement', on_delete=models.CASCADE, null=True)
    month_statement = models.ForeignKey('MonthStatement', on_delete=models.CASCADE, null=True)


class WeekStatement(models.Model):
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE)
    starting_at = models.DateField(null=True, unique=True)
    ending_at = models.DateField(null=True, unique=True)
    total_earned = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    rate_per_ride = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    rate_per_hour = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    rate_per_day = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    total_rides = models.IntegerField(default=0, null=True)
    statement_id = models.CharField(max_length=75, null=True, unique=True)
    month_statement = models.ManyToManyField('MonthStatement', null=True)


class MonthStatement(models.Model):
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE)
    starting_at = models.DateField()
    ending_at = models.DateField()
    total_earned = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    rate_per_ride = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    rate_per_hour = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    rate_per_day = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    total_rides = models.IntegerField(default=0, null=True)


class Driver(models.Model):
    u_user_id = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
        csrf_token = Driver.get_csrf_token(session)
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
        if 'current' in ids:
            ids.remove('current')
        return ids

    @staticmethod
    def get_statement(session, id):
        url = 'https://partners.uber.com/p3/money/statements/view/{}'.format(id)
        statement_response = session.get(url)
        data = json.loads(statement_response.text)
        return data

    def get_u_user_id(self, login_response):
        u_user_id_pattern = '"uuid":"([a-zA-Z0-9\-]+)","'
        u_user_id = re.search(u_user_id_pattern, login_response.text).group(1)
        self.u_user_id = u_user_id

    def get_first_name(self, login_response):
        first_name_pattern = '"firstname":"([A-Z\s\-\.]+)","'
        first_name = re.search(first_name_pattern, login_response.text).group(1)
        self.first_name = first_name

    def get_last_name(self, login_response):
        last_name_pattern = '"lastname":"([A-Z\s\-\.]+)","'
        last_name = re.search(last_name_pattern, login_response.text).group(1)
        self.last_name = last_name

    def save_data(self, session, login_response):
        ids = Driver.get_statement_ids(login_response)
        for statement_id in ids:
            data = Driver.get_statement(session, statement_id)
            print('retreived statement data for: ', statement_id)

            time_zone = dateutil.tz.gettz(data['body']['city']['timezone'])
            trip_earnings = data['body']['driver'].get('trip_earnings', None)

            starting_at = dateutil.parser.parse(data['body']['starting_at']).date()
            w, create = WeekStatement.objects.get_or_create(
                driver=self,
                starting_at=starting_at,
                ending_at=starting_at + datetime.timedelta(days=6)
                )
            w.statement_id = statement_id
            w.save()

            month_start = starting_at.replace(day=1)
            m, create = MonthStatement.objects.get_or_create(
                driver=self,
                starting_at=month_start,
                ending_at=month_start.replace(month=month_start.month + 1) - datetime.timedelta(days=1)
            )
            w.month_statement.add(m)

            weeks_touched = [w]
            days_touched = []
            months_touched = [m]

            if not trip_earnings:
                print('empty statement: ', statement_id)
                continue

            trip_data = trip_earnings['trips']
            for trip in trip_data.keys():
                r = Ride(driver=self, trip_id=trip)
                r.status = trip_data[trip]['status']
                if r.status not in ['canceled', 'driver_canceled']:
                    r.begintrip_at = dateutil.parser.parse(trip_data[trip]['begintrip_at'])
                    r.begintrip_at = r.begintrip_at.replace(tzinfo=time_zone)
                    r.dropoff_at = dateutil.parser.parse(trip_data[trip]['dropoff_at'])
                    r.dropoff_at = r.dropoff_at.replace(tzinfo=time_zone)

                r.total_earned = Decimal(trip_data[trip]['total_earned'])
                r.distance = Decimal(trip_data[trip]['distance'])
                r.request_at = dateutil.parser.parse(trip_data[trip]['request_at'])
                r.request_at = r.request_at.replace(tzinfo=time_zone)
                r.duration = datetime.timedelta(seconds=float(trip_data[trip]['duration']))

                r.date = dateutil.parser.parse(trip_data[trip]['date']).date()

                if r.date.month == m.starting_at.month:
                    r.month_statement = m
                else:
                    new_month_start = r.date.replace(day=1)
                    r.month_statement, c = MonthStatement.objects.get_or_create(
                        driver=self,
                        starting_at=new_month_start,
                        ending_at=new_month_start.replace(
                            month=new_month_start.month + 1
                            ) - datetime.timedelta(days=1)
                    )
                    if r.month_statement not in months_touched:
                        months_touched.append(r.month_statement)

                if r.date <= w.ending_at:
                    r.week_statement = w
                else:
                    r.week_statement, c = WeekStatement.objects.get_or_create(
                        driver=self,
                        starting_at=r.date,
                        ending_at=r.date + datetime.timedelta(days=6)
                    )
                    r.week_statement.save()
                    if r.week_statement not in weeks_touched:
                        weeks_touched.append(r.week_statement)

                r.day_statement, c = DayStatement.objects.get_or_create(
                    driver=self,
                    date=r.date,
                    weekday=r.date.weekday(),
                    week_statement=r.week_statement,
                    month_statement=r.month_statement
                )
                r.day_statement.save()
                if r.day_statement not in days_touched:
                    days_touched.append(r.day_statement)

                r.save()

            for day in days_touched:
                if day.date.month not in months_touched:
                    months_touched.append(day.date.month)

                day.total_rides = day.ride_set.count()
                aggs = day.ride_set.aggregate(Sum('total_earned'),
                                              Min('request_at'),
                                              Max('dropoff_at'))

                day.total_earned = aggs['total_earned__sum']

                earliest_request = aggs['request_at__min']
                latest_dropoff = aggs['dropoff_at__max']
                day.time_worked = latest_dropoff - earliest_request

                day.rate_per_ride = day.total_earned / day.total_rides

                hours = round(Decimal(day.time_worked.total_seconds() / 3600), 2)
                day.rate_per_hour = round((day.total_earned / hours), 2)
                day.save()

            for week in weeks_touched:
                for month in months_touched:
                    if month.starting_at < week.starting_at < month.ending_at:
                        week.month_statement.add(month)
                aggs = week.daystatement_set.aggregate(Sum('total_earned'),
                                                       Sum('total_rides'),
                                                       Avg('rate_per_hour'))
                week.total_earned = aggs['total_earned__sum']
                week.total_rides = aggs['total_rides__sum']
                week.rate_per_ride = week.total_earned / week.total_rides
                week.rate_per_hour = aggs['rate_per_hour__avg']
                week.rate_per_day = week.total_earned / week.daystatement_set.count()
                week.save()

            for month in months_touched:
                aggs = month.daystatement_set.aggregate(Sum('total_earned'),
                                                        Sum('total_rides'),
                                                        Avg('rate_per_hour'))
                days = month.daystatement_set.count()
                month.total_earned = aggs['total_earned__sum']
                month.total_rides = aggs['total_rides__sum']
                month.rate_per_ride = month.total_earned / month.total_rides
                month.rate_per_day = month.total_earned / days
                month.rate_per_hour = aggs['rate_per_hour__avg']
