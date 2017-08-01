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
from .serializers import StopSerializer, RouteSerializer, RouteStationSerializer


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
    """
    Takes a start stop (origin) and an end stop (destination), and returns JSON list containing the lines that connect
    them, or an empty JSON list if there are no connecting lines.

    Pass origin and destination as the StopID of those stops.

    :param request:
    :param origin: First stop
    :param destination: End stop
    :return:
    """

    if request.method == 'GET':
        try:
            stop1 = Stop.objects.get(stop_id=origin)
            stop2 = Stop.objects.get(stop_id=destination)
        except:
            return HttpResponse(status=404)

        sql = '''
                SELECT * FROM bus_routestation r1, bus_routestation r2
                WHERE r1.stop_id = {s1} AND
                  r2.stop_id = {s2} AND
                  r1.route_id = r2.route_id AND
                  r1.order < r2.order
            '''
        rs_query = RouteStation.objects.raw(sql.format(s1=stop1.id, s2=stop2.id))


        routes = set()
        for rs in rs_query:
            routes.add(str(rs.route))

        return JsonResponse(list(routes), safe=False)




def time_estimate(request):

    try:
        origin = request.GET['startStop']
        destination = request.GET['endStop']
        route = request.GET['route']
        pattern = request.GET['pattern']
        hour = request.GET['hour']
        day = request.GET['day']

        origin = int(origin)
        destination = int(destination)
        hour = int(hour)
        day = int(day)

        #format: origin, destination, line, pattern, hour, day
        pred = predict(origin, destination, route, pattern, hour, day)
        pred = str(datetime.timedelta(seconds=pred))

    except:
        return HttpResponse(status=400)

    return JsonResponse({'time': pred})


def route_list(request):
    """
    :param request:
    :return: A list of all the routes
    """
    if request.method == "GET":
        routes = Route.objects.all()
        serializer = RouteSerializer(routes, many=True)
        return JsonResponse(serializer.data, safe=False)



def route_stops(request, route_id, journey_pattern):
    """ Given a route_id and journey_pattern, returns all stops on the route
    """
    route = Route.objects.get(route_id=route_id, journey_pattern=journey_pattern)
    stops = route.stops.all()
    serializer = StopSerializer(stops, many=True)
    return JsonResponse(serializer.data, safe=False)



def middle_stops(request, route_id, journey_pattern, origin, destination):
    """ Given a route_id and journey_pattern, returns all stops on the route between origin and destination
    """
    try:
        stop1 = Stop.objects.get(stop_id=origin)
        stop2 = Stop.objects.get(stop_id=destination)
        route = Route.objects.get(route_id=route_id, journey_pattern=journey_pattern)

        inter1 = RouteStation.objects.get(stop=stop1, route=route)
        inter2 = RouteStation.objects.get(stop=stop2, route=route)
    except:
        return HttpResponse(status=404)

    sql = '''
            SELECT * FROM bus_routestation r
            WHERE r.route_id = {route} AND
              r.order >= {s1} AND
              r.order <= {s2}
        '''

    rs_query = RouteStation.objects.raw(sql.format(route=route.id, s1=inter1.order, s2=inter2.order))

    stops = []
    # print(rs_query)
    for rs in (rs_query):
        stops.append(rs.stop)

    serializer = StopSerializer(stops, many=True)
    return JsonResponse(serializer.data, safe=False)


def accessible_stops(request):
    print("Fuck")

    if request.GET:
        stop_id = request.GET['stop_id']
        stop = Stop.objects.get(stop_id=stop_id)
        routes = stop.route_set.all()
        print(routes)

        stops = set()

        # order = RouteStation.objects.get(stop=stop, route=route).order
        afters = Stop.objects.filter(route__in=routes)

        # for rs in afters:
        #     stops.add(rs.stop)
        # return JsonResponse({'length': len(afters)})

        serializer = StopSerializer(afters, many=True)
        return JsonResponse(serializer.data, safe=False)
        # return JsonResponse({'data': stop_id})
