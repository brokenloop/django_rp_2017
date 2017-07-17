import django
import os

# data analysis and wrangling
os.environ['DJANGO_SETTINGS_MODULE'] = 'DjangoSite.settings'

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

    # temporary variables - for testing only
    line = 15
    pattern = 1
    hour = 9
    day = 2

    day = convert_weekday(day)

    # pred_dir = os.path.dirname(__file__)  # get current directory
    filename = os.path.join(settings.DATA_PATH, 'sklearn_models/line15_all_RF.sav')

    # loading pickled model
    model = pickle.load(open(filename, 'rb'))

    pred1 = query_model1(model, origin, pattern, hour, day)
    pred2 = query_model1(model, destination, pattern, hour, day)

    return (pred2 - pred1)


def query_model1(model, stop, pattern, hour, day):
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
    # pred = int(pred[0].item())

    return pred


def query_model2(model, stop, hour, day):
    params = [{
        'Day': day,
        'Hour': hour,
        'StopID': stop,
    }]

    df = pd.DataFrame(params)

    # making the prediction
    pred = model.predict(df)

    # converting the prediction into an int
    # pred = int(pred[0].item())

    return pred


def convert_weekday(day):
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for i in range(len(weekdays)):
        if weekdays[i] == day:
            return i
    else:
        return int(day)


if __name__=="__main__":
    # print(predict(4596, 6282, 15, 1, 9, 1))

    # model, stop, line, pattern, hour, day


    filename = os.path.join(settings.DATA_PATH, 'sklearn_models/line15_all_RF.sav')
    # loading pickled model
    model = pickle.load(open(filename, 'rb'))

    # print(query_model(model, 6318, 15, 1, 9, 2))
    # print(query_model(model, 1083, 15, 1, 9, 2))
    # print(query_model(model, 6282, 15, 1, 9, 2))

    # print(query_model2(model, 6318, 9, 2))
    # print(query_model2(model, 1083, 9, 2))
    # print(query_model2(model, 6282, 9, 2))
    print(query_model1(model, 6318, 1, 9, 2))
    print(query_model1(model, 1083, 1, 9, 2))
    print(query_model1(model, 6282, 1, 9, 2))

    # print(convert_weekday(2))