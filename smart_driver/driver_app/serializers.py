from rest_framework import serializers
from .models import Ride, Statement, Driver


class RideSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ride
        fields = '__all__'


class StatementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Statement
        fields = ('url', 'statement_id', 'driver', 'starting_at', 'ending_at',
                'total_earned', 'total_fare','total_uber_fee', 'total_surge',
                'trip_count', 'total_distance', 'city', 'ride_set')


class DriverSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Driver
        exclude = 'u_user_id', 'email' 
