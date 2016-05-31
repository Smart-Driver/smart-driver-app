from django.shortcuts import render
from rest_framework import viewsets
from .serializers import RideSerializer, StatementSerializer, DriverSerializer
from .models import Ride, Statement, Driver


class RideViewSet(viewsets.ModelViewSet):
     queryset = Ride.objects.all()
     serializer_class = RideSerializer


class StatementViewSet(viewsets.ModelViewSet):
     queryset = Statement.objects.all()
     serializer_class = StatementSerializer


class DriverViewSet(viewsets.ModelViewSet):
     queryset = Driver.objects.all()
     serializer_class = DriverSerializer
