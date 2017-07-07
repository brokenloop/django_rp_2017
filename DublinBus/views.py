from django.shortcuts import render
from django.http import HttpResponse
from .scripts import predict, convert_weekday
import datetime


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

    return render(request, 'DublinBus/index.html', context)
