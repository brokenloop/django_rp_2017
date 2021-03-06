import datetime
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .scripts import *
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import Stop, Route, RouteStation, Timetable
from .serializers import StopSerializer, RouteSerializer, TimetableSerializer
    # RouteStationSerializer


def index(request):
    return render(request, 'bus/index.html')


def stop_list(request):
    """
    :param request:
    :return: A list of all stops
    """
    if request.method == "GET":
        stops = Stop.objects.all()
        serializer = StopSerializer(stops, many=True)
        return JsonResponse(serializer.data, safe=False)


def get_timetable(request, route_id, journey_pattern, day):
    """
    :param request:
    :param route_id:
    :param journey_pattern:
    :param day:

    :return: a single timetable
    """

    try:
        timetable = Timetable.objects.get(route=route_id, journeypattern=journey_pattern, service=day)
    except Timetable.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TimetableSerializer(timetable)
        return JsonResponse(serializer.data)


def timetable_list(request):
    """
    :param request:
    :return: A list of all timetables
    """

    if request.method == "GET":
        timetables = Timetable.objects.all()
        serializer = TimetableSerializer(timetables, many=True)
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
        weather = request.GET['weather']

        origin = int(origin)
        destination = int(destination)
        hour = int(hour)
        day = int(day)

        #format: origin, destination, line, pattern, hour, day
        pred = predict(origin, destination, route, pattern, hour, day, weather)
        pred = str(datetime.timedelta(seconds=pred))

    except:
        return HttpResponse(status=400)

    return JsonResponse({'time': pred})


def clocktime_estimate(request):
    print("Fuck")

    try:
        origin = request.GET['startStop']
        destination = request.GET['endStop']
        route = request.GET['route']
        pattern = request.GET['pattern']
        hour = request.GET['hour']
        minutes = request.GET['minutes']
        day = request.GET['day']
        weather = request.GET['weather']
    except:
        return HttpResponse(status=400)

    try:
        origin = int(origin)
        destination = int(destination)
        hour = int(hour)
        minutes = int(minutes)
        day = int(day)

        # get_clocktime returns two timedelta objects, origin arrival and destination arrival
        origin_t, destination_t, travel_time = get_clocktime(origin, destination, route, pattern, hour, minutes, day, weather)
    except:
            return HttpResponse(status=500)

    return JsonResponse({'clocktime': (str(origin_t), str(destination_t)), 'travel_time': travel_time})

def routes(request):
    if request.method == "GET":
        routes = Route.objects.all()
        serializer = RouteSerializer(routes, many=True)
        return JsonResponse(serializer.data, safe=False)



def route_list(request):
    """
    :param request:
    :return: A list of all the routes
    """
    if request.method == "GET":
        # routes = Route.objects.all()
        # routes = Route.objects.values("route_id").distinct()
        routes = Route.objects.order_by().values('route_id').distinct()
        route_ids = []
        for value in routes:
            route_ids.append(value)
        # print(route_ids)
        # routes = dict(routes)
        # serializer = RouteSerializer(routes, many=True)
        return JsonResponse(route_ids, safe=False)



def route_stops(request, route_id, journey_pattern):
    """ Given a route_id and journey_pattern, returns all stops on the route
    """
    route = Route.objects.get(route_id=route_id, journey_pattern=journey_pattern)
    # print(route)
    stops = route.stops.all()
    # print(stops)
    serializer = StopSerializer(stops, many=True)
    return JsonResponse(serializer.data, safe=False)


def route_patterns(request, route_id):
    """ Given a route_id, returns the journeyPatterns for the route
    """
    routes = Route.objects.filter(route_id=route_id)
    patterns = []
    for route in routes:
        patterns.append(route.journey_pattern)
    return JsonResponse(patterns, safe=False)


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

def origin_to_end(request, route_id, journey_pattern, origin):
    """ Given a route_id and journey_pattern, returns all stops on the route from the origin to the end of the route
    """
    try:
        stop1 = Stop.objects.get(stop_id=origin)
        route = Route.objects.get(route_id=route_id, journey_pattern=journey_pattern)

        inter1 = RouteStation.objects.get(stop=stop1, route=route)
    except:
        return HttpResponse(status=404)

    sql = '''
            SELECT * FROM bus_routestation r
            WHERE r.route_id = {route} AND
              r.order >= {s1}
        '''

    rs_query = RouteStation.objects.raw(sql.format(route=route.id, s1=inter1.order))

    stops = []
    # print(rs_query)
    for rs in (rs_query):
        stops.append(rs.stop)

    serializer = StopSerializer(stops, many=True)
    return JsonResponse(serializer.data, safe=False)

def accessible_stops(request):

    if request.GET:
        stop_id = request.GET['stop_id']
        stop = Stop.objects.get(stop_id=stop_id)
        routes = stop.route_set.all()
        # print(routes)

        stops = set()

        # order = RouteStation.objects.get(stop=stop, route=route).order
        afters = Stop.objects.filter(route__in=routes)

        # for rs in afters:
        #     stops.add(rs.stop)
        # return JsonResponse({'length': len(afters)})

        serializer = StopSerializer(afters, many=True)
        return JsonResponse(serializer.data, safe=False)
        # return JsonResponse({'data': stop_id})



def cookie(request):
    return render(request, 'bus/cookie.html')
