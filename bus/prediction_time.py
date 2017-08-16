import time
from bus.scripts import *








if __name__ == "__main__":

    print("Start")

    start = time.time()

    origin = 808
    destination = 809
    route = "46A"
    pattern = 1
    hour = 14
    day = 3
    weather = 1
    #
    # for i in range(10):
    #     predict(origin, destination, route, pattern, hour, day, weather)

    filename = os.path.join(settings.DATA_PATH, 'sklearn_models/' + route + '.sav')

    # loading pickled model
    model = pickle.load(open(filename, 'rb'))

    for i in range(1000):
        pred1 = query_model(model, origin, pattern, hour, day, weather)
        pred2 = query_model(model, destination, pattern, hour, day, weather)


    total = time.time() - start

    print("Took", total, "seconds")