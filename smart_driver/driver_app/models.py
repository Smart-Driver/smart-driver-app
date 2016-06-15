import json
import re
import datetime
import dateutil.parser
from dateutil.tz import gettz
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from django.db import models
from django.db.models import Min, Max, Sum, Avg
from django.contrib.auth.models import User


class Ride(models.Model):
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE)
    week_statement = models.ForeignKey('WeekStatement',
                                       on_delete=models.CASCADE, null=True)
    day_statement = models.ForeignKey('DayStatement',
                                      on_delete=models.CASCADE, null=True)
    month_statement = models.ForeignKey('MonthStatement',
                                        on_delete=models.CASCADE, null=True)
    trip_id = models.CharField(max_length=50, primary_key=True)
    status = models.CharField(max_length=15)
    total_earned = models.DecimalField(max_digits=8, decimal_places=2)
    distance = models.DecimalField(max_digits=7, decimal_places=2)
    date = models.DateField()
    request_at = models.DateTimeField()
    begintrip_at = models.DateTimeField(null=True)
    dropoff_at = models.DateTimeField(null=True)
    duration = models.DurationField()

    def get_stats(self, ride_data, time_zone):
        self.date = dateutil.parser.parse(ride_data['date']).date()

        self.status = ride_data['status']
        if self.status not in ['canceled', 'driver_canceled']:
            self.begintrip_at = dateutil.parser.parse(ride_data['begintrip_at'])
            self.begintrip_at = self.begintrip_at.replace(tzinfo=time_zone)
            self.dropoff_at = dateutil.parser.parse(ride_data['dropoff_at'])
            self.dropoff_at = self.dropoff_at.replace(tzinfo=time_zone)

        self.total_earned = Decimal(ride_data['total_earned'])
        self.distance = Decimal(ride_data['distance'])
        self.request_at = dateutil.parser.parse(ride_data['request_at'])
        self.request_at = self.request_at.replace(tzinfo=time_zone)
        self.duration = datetime.timedelta(seconds=float(ride_data['duration']))
        self.save()

    def assign_month(self, months):
        for m in months:
            if self.date.month == m.starting_at.month:
                self.month_statement = m
        if not self.month_statement:
            new_month_start = self.date.replace(day=1)
            self.month_statement, c = MonthStatement.objects.get_or_create(
                driver=self.driver,
                starting_at=new_month_start,
                ending_at=new_month_start + relativedelta(day=31),
                month_name=new_month_start.strftime('%B \'%y')
            )
            months.append(self.month_statement)
        self.save()
        return months

    def assign_week(self, weeks):
        for w in weeks:
            if w.starting_at <= self.date <= w.ending_at:
                self.week_statement = w
        if not self.week_statement:
            self.week_statement, c = WeekStatement.objects.get_or_create(
                driver=self.driver,
                starting_at=self.date,
                ending_at=self.date + datetime.timedelta(days=6)
            )
            weeks.append(self.week_statement)
        self.save()
        return weeks

    def assign_day(self, days):
        for d in days:
            if self.date == d.date:
                self.day_statement = d
        if not self.day_statement:
            self.day_statement, c = DayStatement.objects.get_or_create(
                driver=self.driver,
                date=self.date,
                weekday=self.date.weekday(),
                week_statement=self.week_statement,
                month_statement=self.month_statement
            )
            days.append(self.day_statement)
        self.save()
        return days


class DayStatement(models.Model):
    WEEKDAY_CHOICES = ((0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'),
                       (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'),
                       (6, 'Sunday'))
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE)
    total_rides = models.IntegerField(default=0, null=True)
    total_earned = models.DecimalField(max_digits=8, decimal_places=2,
                                       null=True)
    date = models.DateField()
    weekday = models.IntegerField(choices=WEEKDAY_CHOICES, default=0)
    time_worked = models.DurationField(null=True)
    rate_per_ride = models.DecimalField(max_digits=8, decimal_places=2,
                                        null=True)
    rate_per_hour = models.DecimalField(max_digits=8, decimal_places=2,
                                        null=True)
    week_statement = models.ForeignKey('WeekStatement',
                                       on_delete=models.CASCADE, null=True)
    month_statement = models.ForeignKey('MonthStatement',
                                        on_delete=models.CASCADE, null=True)

    def calculate_day_stats(self):
        self.total_rides = self.ride_set.count()
        aggs = self.ride_set.aggregate(Sum('total_earned'),
                                       Min('request_at'),
                                       Max('dropoff_at'))

        self.total_earned = aggs['total_earned__sum']
        self.rate_per_ride = self.total_earned / self.total_rides

        earliest_request = aggs['request_at__min']
        latest_dropoff = aggs['dropoff_at__max']
        if latest_dropoff:
            self.time_worked = latest_dropoff - earliest_request
            hours = round(Decimal(self.time_worked.total_seconds() / 3600), 2)
            self.rate_per_hour = round((self.total_earned / hours), 2)
        self.save()


class WeekStatement(models.Model):
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE)
    starting_at = models.DateField(null=True, unique=True)
    ending_at = models.DateField(null=True, unique=True)
    total_earned = models.DecimalField(max_digits=8, decimal_places=2,
                                       null=True)
    rate_per_ride = models.DecimalField(max_digits=8, decimal_places=2,
                                        null=True)
    rate_per_hour = models.DecimalField(max_digits=8, decimal_places=2,
                                        null=True)
    rate_per_day = models.DecimalField(max_digits=8, decimal_places=2,
                                       null=True)
    total_rides = models.IntegerField(default=0, null=True)
    statement_id = models.CharField(max_length=75, null=True, unique=True)
    month_statement = models.ManyToManyField('MonthStatement')

    def associate_months(self, months):
        for month in months:
            if month.starting_at.month in [self.starting_at.month,
                                           self.ending_at.month]:
                self.month_statement.add(month)
                self.save()

    def calculate_week_stats(self):
        days = self.daystatement_set.count()
        if days:
            aggs = self.daystatement_set.aggregate(Sum('total_earned'),
                                                   Sum('total_rides'),
                                                   Avg('rate_per_hour'))
            self.total_earned = aggs['total_earned__sum']
            self.total_rides = aggs['total_rides__sum']
            self.rate_per_ride = self.total_earned / self.total_rides
            self.rate_per_hour = aggs['rate_per_hour__avg']
            self.rate_per_day = self.total_earned / days
            self.save()


class MonthStatement(models.Model):
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE)
    starting_at = models.DateField()
    ending_at = models.DateField()
    month_name = models.CharField(max_length=15)
    total_earned = models.DecimalField(max_digits=8, decimal_places=2,
                                       null=True)
    rate_per_ride = models.DecimalField(max_digits=8, decimal_places=2,
                                        null=True)
    rate_per_hour = models.DecimalField(max_digits=8, decimal_places=2,
                                        null=True)
    rate_per_day = models.DecimalField(max_digits=8, decimal_places=2,
                                       null=True)
    total_rides = models.IntegerField(default=0, null=True)

    def calculate_month_stats(self):
        days = self.daystatement_set.count()
        if days:
            aggs = self.daystatement_set.aggregate(Sum('total_earned'),
                                                   Sum('total_rides'),
                                                   Avg('rate_per_hour'))
            self.total_earned = aggs['total_earned__sum']
            self.total_rides = aggs['total_rides__sum']
            self.rate_per_ride = self.total_earned / self.total_rides
            self.rate_per_day = self.total_earned / days
            self.rate_per_hour = aggs['rate_per_hour__avg']
            self.save()


class Driver(models.Model):
    u_user_id = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    def get_name(self):
        return self.first_name.title() + ' ' + self.last_name.title()

    @staticmethod
    def get_csrf_token(session):
        login_response = session.get('https://login.uber.com/login')
        csrf_token_pattern = (
            'type="hidden" name="_csrf_token" value="([a-zA-Z0-9\_\-\=]+)">')
        csrf_token = re.search(
            csrf_token_pattern, login_response.text).group(1)
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
    def get_statement(session, id):
        url = 'https://partners.uber.com/p3/money/statements/view/{}'.format(
            id)
        statement_response = session.get(url)
        data = json.loads(statement_response.text)
        return data

    def get_u_user_id(self, login_response):
        u_user_id_pattern = '"uuid":"([a-zA-Z0-9\-]+)","'
        u_user_id = re.search(u_user_id_pattern, login_response.text).group(1)
        self.u_user_id = u_user_id

    def get_first_name(self, login_response):
        first_name_pattern = '"firstname":"([A-Z\s\-\.]+)","'
        first_name = re.search(
            first_name_pattern, login_response.text).group(1)
        self.first_name = first_name

    def get_last_name(self, login_response):
        last_name_pattern = '"lastname":"([A-Z\s\-\.]+)","'
        last_name = re.search(last_name_pattern, login_response.text).group(1)
        self.last_name = last_name

    @staticmethod
    def get_statement_ids(login_response):
        cream_id_pattern = '"cream_invoice_uuid":"([a-zA-Z0-9\-]+)","'
        ids = re.findall(cream_id_pattern, login_response.text)
        if 'current' in ids:
            ids.remove('current')
        return ids

    def get_new_statement_ids(self, ids):
        stored_ids = {ws.statement_id for ws in self.weekstatement_set.all()}
        new = set(ids) - stored_ids
        return list(new)

    def grab_data(self, session, ids):
        for statement_id in ids:
            data = Driver.get_statement(session, statement_id)
            print('retreived statement data for: ', statement_id)

            time_zone = gettz(data['body']['city']['timezone'])
            trip_earnings = data['body']['driver'].get('trip_earnings', None)

            starting_at = dateutil.parser.parse(
                data['body']['starting_at']).date()
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
                ending_at=month_start + relativedelta(day=31),
                month_name=month_start.strftime('%B \'%y')
            )
            w.month_statement.add(m)
            w.save()

            weeks_touched = [w]
            days_touched = []
            months_touched = [m]

            if not trip_earnings:
                print('empty statement: ', statement_id)
                continue

            for trip in trip_earnings['trips'].keys():
                r = Ride(driver=self, trip_id=trip)

                r.get_stats(trip_earnings['trips'][trip], time_zone)

                months_touched = r.assign_month(months_touched)
                weeks_touched = r.assign_week(weeks_touched)
                days_touched = r.assign_day(days_touched)

            for day in days_touched:
                day.calculate_day_stats()

            for week in weeks_touched:
                week.associate_months(months_touched)
                week.calculate_week_stats()

            for month in months_touched:
                month.calculate_month_stats()
