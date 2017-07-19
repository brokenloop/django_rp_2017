import django
import sys, os, csv

# ----- are these even necessary? ----- 
# change this to your own path if you are running the program
# project_path = "~Desktop/compsci/ResearchPracticum/DjangoSite/"

# sys.path.append(project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'DjangoSite.settings'
django.setup()

from django.conf import settings
from bus.models import Stop, Route, RouteStation


def populate_stops(csv_path):

    with open(csv_path) as f:
        reader = csv.reader(f)

        # skip first line, as this is the header
        next(reader)

        for row in reader:
            index = row[0]
            stop_id = row[1]
            name = row[2] + " - " + row[3]
            lat = row[4]
            lon = row[5]

            obj, created = Stop.objects.get_or_create(
                stop_id=row[1],
                name=row[2] + " - " + row[3],
                lat=row[4],
                lon=row[5],
            )

            if (created):
                print(stop_id, "created")
            else:
                print(stop_id, "already exists")


def populate_routes(csv_path):

    with open(csv_path) as f:
        reader = csv.reader(f)

        # skip first line, as this is the header
        next(reader)

        for row in reader:
            index = row[0]
            route_id = row[1]
            journey_pattern = str(row[2])

            obj, created = Route.objects.get_or_create(
                route_id=route_id,
                journey_pattern=journey_pattern,
            )

            if created:
                print(route_id, "-", journey_pattern, "created")
            else:
                print(route_id, "already exists")


def populate_route_stations(csv_path):
    missing_stops = set()
    missing_routes = set()

    with open(csv_path) as f:
        reader = csv.reader(f)

        # skip first line, as this is the header
        next(reader)

        for row in reader:
            index = row[0]
            StopID = row[1]
            Runtime = str(row[2])
            Order = row[3]
            LineID = row[4]
            JourneyPatternID = int(float(row[5]))
            lon = row[6]
            lat = row[7]

            try:
                stop = Stop.objects.get(
                    stop_id=StopID
                )

                route = Route.objects.get(
                    route_id=LineID,
                    journey_pattern=JourneyPatternID
                )

                route_stop, created = RouteStation.objects.get_or_create(
                    stop=stop,
                    route=route,
                    order=Order,
                )

                # if created:
                #     print(stop, route, "created")
                # else:
                #     print(stop, route, "already exists")
            except:
                print("Error!")


    return missing_stops, missing_routes


if __name__=="__main__":
    stop_path = os.path.join(settings.DATA_PATH, 'static_data/stops_all.csv')
    route_path = os.path.join(settings.DATA_PATH, 'static_data/routes_all.csv')
    routestops_path = os.path.join(settings.DATA_PATH, 'static_data/route_stops_all.csv')

    populate_stops(stop_path)
    populate_routes(route_path)
    populate_route_stations(routestops_path)


