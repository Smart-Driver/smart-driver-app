import datetime
from rest_framework import serializers
from .models import Ride, DayStatement, WeekStatement, Driver, MonthStatement


class RideSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ride
        fields = ('date', 'status', 'total_earned', 'request_at')


class DayStatementSerializer(serializers.HyperlinkedModelSerializer):
    date = serializers.SerializerMethodField()
    weekday = serializers.SerializerMethodField()
    total_earned = serializers.SerializerMethodField()
    rate_per_ride = serializers.SerializerMethodField()
    rate_per_hour = serializers.SerializerMethodField()

    class Meta:
        model = DayStatement
        fields = ('date', 'weekday', 'total_earned', 'time_worked',
                  'rate_per_hour', 'total_rides', 'rate_per_ride')

    def get_date(self, obj):
        return obj.date.strftime('%b %d, %Y')

    def get_weekday(self, obj):
        return obj.get_weekday_display()

    def get_total_earned(self, obj):
        return "$" + str(obj.total_earned)

    def get_rate_per_ride(self, obj):
        return "$" + str(obj.rate_per_ride)

    def get_rate_per_hour(self, obj):
        return "$" + str(obj.rate_per_hour)


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
