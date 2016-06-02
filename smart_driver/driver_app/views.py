import requests
from django.shortcuts import render
from rest_framework import viewsets
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
     queryset = DayStatement.objects.all()
     serializer_class = DayStatementSerializer


class WeekStatementViewSet(viewsets.ModelViewSet):
     queryset = WeekStatement.objects.all()
     serializer_class = WeekStatementSerializer


class DriverViewSet(viewsets.ModelViewSet):
     queryset = Driver.objects.all()
     serializer_class = DriverSerializer


def home(request):
    if request.POST:
        username = request.POST['email']
        password = request.POST['password']

        session = requests.Session()
        login_response = Driver.login(session, request)

        if login_response.status_code == 200:
            user, created = User.objects.get_or_create(username=username)

            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)


    return render(request, "driver_app/home.html")


def profile(request):
    return render (request, "driver_app/profile.html")
