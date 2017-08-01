import django
import os

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

def predict(origin, destination, line, pattern, hour, day):
    """ Predicts time taken to get from origin to destination, using query_model
    """

    day = convert_weekday(day)

    # loading pickled model
    filename = os.path.join(settings.DATA_PATH, 'sklearn_models/line15_all_RF.sav')
    model = pickle.load(open(filename, 'rb'))

    pred1 = query_model(model, origin, pattern, hour, day)
    pred2 = query_model(model, destination, pattern, hour, day)

    return (pred2 - pred1)


def query_model(model, stop, pattern, hour, day):
    """ Queries the Random Forest model, returning an estimate for how long it will take to reach that stop
    """

    params = [{
        'Day': day,
        'Hour': hour,
        'JourneyPatternID': pattern,
        'StopID': stop,
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


if __name__=="__main__":


    # loading pickled model
    # filename = os.path.join(settings.DATA_PATH, 'sklearn_models/line15_all_RF.sav')
    # model = pickle.load(open(filename, 'rb'))
    #
    print(predict(6282, 1083, 15, 1, 15, 4))
    # origin = Stop.objects.get(stop_id=4886)
    # destination = Stop.objects.get(stop_id=1166)
    # route_15 = Route.objects.get(route_id=15, journey_pattern=1)

    # print(connected(origin, destination, route_15))
    # stops = route_15.stops.all()
    # print(stops)





