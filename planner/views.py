from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from bus.models import Stop
from bus.serializers import StopSerializer
import requests
from bus.views import stop_list as bus_stop_list
from bus.models import *
from bus.scripts import *
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
                    pattern = 1
                    num_stops = leg["transit_details"]["num_stops"]
                    hour = 5
                    day = 2
                    weather = 1

                    # print(route_id)
                    route = Route.objects.get(route_id=route_id, journey_pattern=1)
                    origin = RouteStation.objects.get(order=0, route=route).stop.stop_id
                    destination = RouteStation.objects.get(order=num_stops, route=route).stop.stop_id
                    travel_time = predict(origin, destination, route_id, pattern, hour, day, weather)

                    minutes, seconds = divmod(travel_time, 60)
                    hours, minutes = divmod(minutes, 60)

                    print()
                    print("Origin", origin)
                    print("Destination", destination)
                    print(type(origin))
                    print(type(destination))

                    print(travel_time)
        except:
            print("Route", route_id, "not found")


        # Replace durations with our own estimates

        return JsonResponse(response)
        # return HttpResponse("success")


 # if request.method == "GET":
 #        stops = Stop.objects.all()
 #        serializer = StopSerializer(stops, many=True)
 #        return JsonResponse(serializer.data, safe=False)