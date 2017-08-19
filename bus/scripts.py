import django
import os
import cProfile

os.environ['DJANGO_SETTINGS_MODULE'] = 'DjangoSite.settings'
django.setup()

from django.conf import settings
from bus.models import Stop, Route, RouteStation

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
    cProfile.run(1 + 1)
    # stops = route_15.stops.all()
    # print(stops)





