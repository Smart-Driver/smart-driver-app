import requests
from django.shortcuts import render
from rest_framework import viewsets
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


def login(request):
    if request.POST:

        session = requests.Session()
        login_response = Driver.login(session)

        if login_response.status == 200:
            Driver.save_data(session, login_response)

        # username = request.POST['email']
        # User.get_or_create(username=username)
