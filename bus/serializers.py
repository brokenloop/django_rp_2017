from rest_framework import serializers
from .models import Stop, Route, RouteStation, Timetable


class StopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stop
        fields = ('id', 'lat', 'lon', 'name', 'stop_id')


# class StopLocationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Stop
#         fields = ('stop_id', 'lat', 'lon')


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ('id', 'route_id', 'journey_pattern', 'headsign')


class RouteStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteStation
        fields = ('stop', 'route', 'order')


class TimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timetable
        fields = ('route_id', 'day', 'departure', 'journey_pattern')















