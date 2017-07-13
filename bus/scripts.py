# data analysis and wrangling
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

# change this to the correct path on your machine

def predict(stop, hour, day):

    day = convert_weekday(day)

    # pred_dir = os.path.dirname(__file__)  # get current directory
    filename = os.path.join(settings.DATA_PATH, 'sklearn_models/line15_RF.sav')

    # loading pickled model
    model = pickle.load(open(filename, 'rb'))

    # creating the dataframe
    params = [{
        'Day': day,
        'Hour': hour,
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


if __name__=="__main__":
    print(predict(1, 14, 4596))