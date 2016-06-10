import json
import requests
import datetime
from django.shortcuts import render
from rest_framework import viewsets
from django.http import HttpResponseRedirect
from django.db.models import Avg
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .serializers import RideSerializer, DayStatementSerializer
from .serializers import WeekStatementSerializer, MonthStatementSerializer
from .serializers import DriverSerializer
from .models import Ride, DayStatement, WeekStatement, MonthStatement, Driver


class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer


class DayStatementViewSet(viewsets.ModelViewSet):
    queryset = DayStatement.objects.filter(total_earned__gt=0)
    serializer_class = DayStatementSerializer

    def get_queryset(self):
        queryset = DayStatement.objects.filter(total_earned__gt=0).order_by('-date')
        driver_id = self.request.query_params.get('driver', None)
        month = self.request.query_params.get('month', None)
        weekday = self.request.query_params.get('weekday', None)
        if driver_id:
            queryset = queryset.filter(driver=Driver.objects.get(id=driver_id))
        if month:
            queryset = queryset.filter(month_statement=MonthStatement.objects.get(month_name=month))
        if weekday:
            for tup in DayStatement.WEEKDAY_CHOICES:
                if tup[1] == weekday:
                    queryset = queryset.filter(weekday=tup[0])
        return queryset


class WeekStatementViewSet(viewsets.ModelViewSet):
    queryset = WeekStatement.objects.filter(total_earned__gt=0)
    serializer_class = WeekStatementSerializer

    def get_queryset(self):
        queryset = WeekStatement.objects.filter(total_earned__gt=0).order_by('-starting_at')
        driver_id = self.request.query_params.get('driver', None)
        month = self.request.query_params.get('month', None)
        if driver_id:
            queryset = queryset.filter(driver=Driver.objects.get(id=driver_id))
        if month:
            queryset = queryset.filter(month_statement=MonthStatement.objects.get(month_name=month))
        return queryset


class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer


class MonthStatementViewSet(viewsets.ModelViewSet):
    queryset = MonthStatement.objects.filter(total_earned__gt=0).order_by('-starting_at')
    serializer_class = MonthStatementSerializer


def home(request):
    context = {}
    if request.POST:
        username = request.POST['email']
        password = request.POST['password']

        session = requests.Session()
        login_response = Driver.login(session, request)

        if login_response.status_code == 200:
            user, created = User.objects.get_or_create(username=username)

            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

            ids = Driver.get_statement_ids(login_response)

            if created:
                driver = Driver(user=user, email=username)
                driver.get_u_user_id(login_response)
                driver.get_first_name(login_response)
                driver.get_last_name(login_response)
                driver.save()

            else:
                driver = Driver.objects.get(user=user)
                ids = driver.get_new_statement_ids(ids)

            driver.grab_data(session, ids)
            return HttpResponseRedirect("/profile/")

        else:
            print('login_failed')
            context['fail'] = login_response.status_code

    return render(request, "driver_app/home.html", context)


def profile(request):
    driver = Driver.objects.get(user=request.user)
    day_statements = DayStatement.objects.filter(
        driver=driver).filter(total_earned__gt=0)

    hourly_rate_by_weekday = {'key':"Hourly Rate By Weekday", 'values':[]}

    rate_avgs = day_statements.values('weekday').annotate(avg=Avg('rate_per_hour'))
    rate_avgs = sorted(rate_avgs, key=lambda lil_dict: lil_dict['weekday'])
    max_avg = max(rate_avgs, key=lambda lil_dict: lil_dict['avg'])['avg']
    hourly_rate_by_weekday['values'] = [{
        "label": dict(DayStatement.WEEKDAY_CHOICES)[day_dict['weekday']],
        "value": round(day_dict['avg'], 2)
        } for day_dict in rate_avgs]


    context = {'weekday_graph_data': json.dumps(hourly_rate_by_weekday),
               'hourly_max': round(max_avg)}
    return render(request, "driver_app/profile.html", context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")
