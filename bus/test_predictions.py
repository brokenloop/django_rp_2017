import time
from .scripts import *








if __name__ == "__main__":

    start = time.time()

    origin = 808
    destination = 2031
    route = "46A"
    pattern = 1
    hour = 14
    day = 3
    weather = 1

    for i in range(10):
        predict(origin, destination, route, pattern, hour, day, weather)

    total = time.time() - start

    print("Took", total, "seconds")