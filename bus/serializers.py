from rest_framework import serializers
from .models import Stop, Route, RouteStation


class StopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stop
        fields = ('id', 'lat', 'lon', 'name', 'stop_id')


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ('id', 'route_id', 'journey_pattern', 'stops')
















