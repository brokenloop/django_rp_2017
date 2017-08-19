from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from bus.models import Stop
from bus.serializers import StopSerializer
import requests
from bus.views import stop_list as bus_stop_list


def index(request):
    return render(request, 'planner/index.html')
    # return HttpResponse("Hello, world. You're at the polls index.")


def stop_list(request):
    return bus_stop_list(request)


def get_directions(request):
    if request.method == "GET":
        params = {
            "origin": request.GET["origin"],
            "destination": request.GET["destination"],
            "key": request.GET["key"],
            "mode": request.GET["mode"],
            "transit_mode": request.GET["transit_mode"],
        }

        url = "https://maps.googleapis.com/maps/api/directions/json"
        response = requests.get(url, params=params).json()
        return JsonResponse(response)
        # return HttpResponse("success")


 # if request.method == "GET":
 #        stops = Stop.objects.all()
 #        serializer = StopSerializer(stops, many=True)
 #        return JsonResponse(serializer.data, safe=False)