from rest_framework import serializers
from .models import Ride, DayStatement, WeekStatement, Driver, MonthStatement


class RideSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ride
        fields = ('date', 'status', 'total_earned', 'request_at')


class DayStatementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DayStatement
        fields = ('date', 'weekday', 'total_earned', 'time_worked',
                  'rate_per_hour', 'total_rides', 'rate_per_ride')


class WeekStatementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WeekStatement
        fields = ('starting_at', 'ending_at', 'total_earned', 'rate_per_day',
                  'rate_per_hour', 'total_rides', 'rate_per_ride')


class DriverSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Driver
        exclude = 'u_user_id', 'email', 'user'

class MonthStatementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MonthStatement
        fields = ('month_name', 'total_earned', 'rate_per_day',
                  'rate_per_hour', 'total_rides','rate_per_ride')
