from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from bus.models import Stop
from bus.serializers import StopSerializer
import requests
from bus.views import stop_list as bus_stop_list
from bus.models import *
import pprint as pp


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

        legs = response["routes"][0]["legs"][0]["steps"]

        try:
            for leg in legs:
                if leg["travel_mode"] == "TRANSIT":
                    pp.pprint(leg)
                    route_id = leg["transit_details"]["line"]["short_name"]
                    num_stops = leg["transit_details"]["num_stops"]
                    # print(route_id)
                    route = Route.objects.get(route_id=route_id, journey_pattern=1)
                    origin = RouteStation.objects.get(order=0, route=route)
                    destination = RouteStation.objects.get(order=num_stops, route=route)
        except:
            print("")


        # Replace durations with our own estimates

        return JsonResponse(response)
        # return HttpResponse("success")


 # if request.method == "GET":
 #        stops = Stop.objects.all()
 #        serializer = StopSerializer(stops, many=True)
 #        return JsonResponse(serializer.data, safe=False)