import requests
from django.shortcuts import render
from rest_framework import viewsets
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .serializers import RideSerializer, DayStatementSerializer
from .serializers import WeekStatementSerializer, DriverSerializer
from .models import Ride, DayStatement, WeekStatement, Driver


class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer


class DayStatementViewSet(viewsets.ModelViewSet):
    #DayStatement.objects.filter(driver=driver).order_by('-date')
    queryset = DayStatement.objects.all()
    serializer_class = DayStatementSerializer


class WeekStatementViewSet(viewsets.ModelViewSet):
    queryset = WeekStatement.objects.all()
    serializer_class = WeekStatementSerializer


class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer


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
            context['fail'] = True

    return render(request, "driver_app/home.html", context)


def profile(request):
    driver = Driver.objects.get(user=request.user)
    statements = DayStatement.objects.filter(driver=driver).order_by('date')

    context = {'statements': statements}

    return render(request, "driver_app/profile.html", context)
