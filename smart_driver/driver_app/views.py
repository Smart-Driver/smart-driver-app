from django.shortcuts import render
from rest_framework import viewsets
from django.views.generic.base import TemplateView
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


class HomeView(TemplateView):
    template_name = "driver_app/home.html"
