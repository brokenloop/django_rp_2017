import django
import os
import datetime
import bisect
import profile

os.environ['DJANGO_SETTINGS_MODULE'] = 'DjangoSite.settings'
django.setup()

from django.conf import settings
from bus.models import Stop, Route, RouteStation, Timetable
import pandas as pd
import numpy as np
import os
from django.conf import settings

# machine learning
from sklearn.ensemble import RandomForestRegressor
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.model_selection import train_test_split
# from sklearn import metrics
# from sklearn import *

# pickling
import pickle


def predict(origin, destination, line, pattern, hour, day, weather):
    """ Predicts time taken to get from origin to destination, using query_model
    """

    day = convert_weekday(day)

    filename = os.path.join(settings.DATA_PATH, 'sklearn_models/' + line + '.sav')

    # loading pickled model
    model = pickle.load(open(filename, 'rb'))

    pred1 = query_model(model, origin, pattern, hour, day, weather)
    pred2 = query_model(model, destination, pattern, hour, day, weather)

    return (pred2 - pred1)


def find_service_type(day):
    if day == "Sunday":
        return "sunday"
    elif day == "Saturday":
        return "saturday"
    else:
        return "weekday"


def get_departure_times(route, service, journeypattern, time):
    print("time", time)
    t1 = str(time)
    t1 = "0" + t1 if (len(t1) <= 1) else t1
    print("time", t1)
    t2 = str(int(t1)+1) if int(t1) < 23 else str("00")
    t0 = str(int(t1)-1) if int(t1) != 0 else str("23")
    print("t0:", t0, "  t1:", t1, "  t2:", t2)

    #add leading zero to string of t0 and t2
    t0 = "0" + t0 if (len(t0) <= 1) else str(t0)
    t2 = "0" + t2 if (len(t2) <= 1) else str(t2)
    print("t0:", t0, "  t1:", t1, "  t2:", t2)

    t0_query = Timetable.objects.filter(route_id=route, day=service, journey_pattern=journeypattern, departure__startswith=t0).only("departure")
    t1_query = Timetable.objects.filter(route_id=route, day=service, journey_pattern=journeypattern, departure__startswith=t1).only("departure")
    t2_query = Timetable.objects.filter(route_id=route, day=service, journey_pattern=journeypattern, departure__startswith=t2).only("departure")

    departure_list = list(t0_query) + list(t1_query) + list(t2_query)
    print(departure_list)
    return departure_list


def get_clocktime(origin, destination, line, pattern, hour, minutes, day, weather):
    """
    For a given query finds the ideal terminus departure time using query_model
    """
    current_time = datetime.timedelta(hours=hour, minutes=minutes)

    day = convert_weekday(day)

    filename = os.path.join(settings.DATA_PATH, 'sklearn_models/' + line + '.sav')

    # loading pickled model
    model = pickle.load(open(filename, 'rb'))

    pred1 = query_model(model, origin, pattern, hour, day, weather)
    pred2 = query_model(model, destination, pattern, hour, day, weather)

    travel_time = seconds_to_string(pred2 - pred1)
    ideal_departure = datetime.timedelta.total_seconds(current_time) - pred1
    ideal_hour = int(ideal_departure)//3600

    service = find_service_type(day)
    times = get_departure_times(line, service, pattern, ideal_hour)

    if not times:
        return "No Service:", "No bus at this time", "N/A"
    # times = get_departure_times(line, service, pattern, hour)

    seconds = []

    for t in times:
        t = str(t).split("-")[-1].strip()
        hrs, mins = t.split(":")

        time = datetime.timedelta(hours=int(hrs), minutes=int(mins))
        seconds.append(datetime.timedelta.total_seconds(time))
    seconds.sort()

    # current time minus the time it takes to arrive is the ideal departure time

    # best actual departure time is the closest one before the ideal departure time
    best_index = bisect.bisect_left(seconds, ideal_departure)

    if len(seconds) > best_index:
        best_departure = datetime.timedelta(seconds=seconds[best_index])
    else:
        return "No Service:", "No bus at this time", "N/A"

    #clocktime arrival at origin and destination
    origin_arrival = best_departure + datetime.timedelta(seconds=pred1)
    destination_arrival = origin_arrival+datetime.timedelta(seconds=pred2)

    if destination_arrival > datetime.timedelta(days=1):
        destination_arrival -= datetime.timedelta(days=1)

    print("pred1", datetime.timedelta(seconds=pred1))
    print("pred2", datetime.timedelta(seconds=pred2))
    print("seconds", seconds)
    print("ideal_hour", ideal_hour)
    print("ideal_departure", datetime.timedelta(seconds=ideal_departure))
    print("ideal_departure", ideal_departure)
    print("best_index", best_index)
    print("best_departure", best_departure)
    print("current_time", current_time)
    print("origin_arrival", origin_arrival)
    print("destination_arrival", destination_arrival)

    return origin_arrival, destination_arrival, travel_time


def query_model(model, stop, pattern, hour, day, weather):
    """ Queries the Random Forest model, returning an estimate for how long it will take to reach that stop
    """

    params = [{
        'Day': day,
        'Hour': hour,
        'JourneyPatternID': pattern,
        'StopID': stop,
        "Rain": weather,
    }]

    df = pd.DataFrame(params)

    # making the prediction
    pred = model.predict(df)

    # converting the prediction into an int
    pred = int(pred[0].item())

    return pred


def convert_weekday(day):
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for i in range(len(weekdays)):
        if weekdays[i] == day:
            return i
    else:
        return int(day)


def connected(origin, destination, route):
    """
    :param origin: StopID for the first station
    :param destination: StopID for the second station
    :return: bool, indicating whether the destination is accessible via the origin
    """

    try:
        origin_rs = RouteStation.objects.get(stop=origin, route=route)
        dest_rs = RouteStation.objects.get(stop=destination, route=route)
    except RouteStation.DoesNotExist:
        return False
    return origin_rs.order < dest_rs.order


# def get_common(origin, destination):
#     try:
#         stop1 = Stop.objects.get(stop_id=origin)
#         stop2 = Stop.objects.get(stop_id=destination)
#     except Stop.DoesNotExist:
#         return "None"
#
#     routes1 = stop1.route_set.all()
#     routes2 = stop2.route_set.all()
#     common = routes1 & routes2
#     common = [[route.route_id, route.journey_pattern] for route in common if connected(stop1, stop2, route)]
#
#     return common

def get_common(origin, destination):
    stop1 = Stop.objects.get(stop_id=origin)
    stop2 = Stop.objects.get(stop_id=destination)

    sql = '''
        SELECT * FROM bus_routestation r1, bus_routestation r2
        WHERE r1.stop_id = {s1} AND
          r2.stop_id = {s2} AND
          r1.route_id = r2.route_id AND
          r1.order < r2.order
    '''
    rs_query = RouteStation.objects.raw(sql.format(s1=stop1.id, s2=stop2.id))

    route_list = set()

    for rs in rs_query:
        route_list.add(str(rs.route))

    # route_list = []
    #
    # for rs in rs_query:
    #     if not str(rs.route) in route_list:
    #         route_list.append(str(rs.route))

    print(list(route_list))

    # sql = '''
    #         SELECT r1.name FROM bus_stop r1
    #         WHERE r1.stop_id = {s1}
    #     '''
    # rs_query = RouteStation.objects.raw(sql.format(s1=stop1.id))
    # print(rs_query)


def seconds_to_string(total_seconds):
    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)

    if seconds > 30:
        minutes = minutes + 1

    if hours == 1:
        hour_str = (str(hours) + " hour ")
    elif hours > 1:
        hour_str = (str(hours) + " hours ")
    else:
        hour_str = ""

    minute_str = (str(minutes) + " mins") if (minutes > 0) else ""

    return hour_str + minute_str



if __name__=="__main__":

    # loading pickled model
    # filename = os.path.join(settings.DATA_PATH, 'sklearn_models/line15_all_RF.sav')
    # model = pickle.load(open(filename, 'rb'))
    #
    # print(predict(6282, 1083, 15, 1, 9, 1))
    # origin = Stop.objects.get(stop_id=4886)
    # destination = Stop.objects.get(stop_id=1166)
    # route_15 = Route.objects.get(route_id=15, journey_pattern=1)

    # print(connected(origin, destination, route_15))
    # get_common(4886, 1166)
    # stops = route_15.stops.all()
    # print(stops)
    # a, b = get_clocktime(808, 2035, "46A", 1, 17, 30, 1, False)
    # a, b = get_clocktime(395, 2729, "56A", 1, 11, 42, 3, False)
    a, b = get_clocktime(395, 2729, "15", 1, 7, 25, 3, False)


    print(a)
    print(b)



