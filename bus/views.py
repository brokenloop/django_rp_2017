import datetime
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .scripts import *
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import Stop, Route, RouteStation
from .serializers import StopSerializer, RouteSerializer


def index(request):
    pred = 0
    day = 0
    hour = 0
    stop = 0

    if request.GET:
        # day = convert_weekday(request.GET["day"])
        day = request.GET["day"]
        hour = int(request.GET["hour"])
        stop = int(request.GET["stop"])
        pred = predict(stop, hour, day)
        pred = str(datetime.timedelta(seconds=pred))
        # pred = return_number(stop, hour, day)

        print("Variables")
        print(request.GET)
        print("\n\n")


    else:
        print("None!\n\n")

    # route = request.GET["route"]

    context = {
        "user_options": {
            "day": day,
            "hour": hour,
            "stop": stop,
        },
        "form_selects": {
            "stop": [1270, 665, 4870, 4869, 3007, 6283, 6282],
            "hour": [x for x in range(6, 24)],
            "day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "weather": ["Sunny", "Rainy"],
        },
        "time_prediction": str(pred),
    }

    return render(request, 'bus/index.html', context)


def stop_list(request):
    """
    :param request:
    :return: A list of all stops
    """
    if request.method == "GET":
        stops = Stop.objects.all()
        serializer = StopSerializer(stops, many=True)
        return JsonResponse(serializer.data, safe=False)


def stop_detail(request, stop_id):
    try:
        stop = Stop.objects.get(stop_id=stop_id)
    except Stop.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = StopSerializer(stop)
        return JsonResponse(serializer.data)


def common_routes(request, origin, destination):
    try:
        stop1 = Stop.objects.get(stop_id=origin)
        stop2 = Stop.objects.get(stop_id=destination)
    except:
        return HttpResponse(status=404)

    if request.method == 'GET':
        routes1 = stop1.route_set.all()
        routes2 = stop2.route_set.all()
        common = routes1 & routes2
        common = [route for route in common if connected(stop1, stop2, route)]

        serializer = RouteSerializer(common, many=True)
        return JsonResponse(serializer.data, safe=False)


def time_estimate(request):
    stop = request.GET['endStop']
    hour = request.GET['hour']
    day = request.GET['day']

    try:
        stop = int(stop)
        hour = int(hour)
        day = int(day)

        pred = predict(stop, hour, day)
        pred = str(datetime.timedelta(seconds=pred))

    except:
        return HttpResponse(status=400)

    return JsonResponse({'time': pred,
                         'stop': stop,
                         'hour': hour,
                         'day': day,
                         })


def route_list(request):
    """
    :param request:
    :return: A list of all the routes
    """
    if request.method == "GET":
        routes = Route.objects.all()
        serializer = RouteSerializer(routes, many=True)
        return JsonResponse(serializer.data, safe=False)