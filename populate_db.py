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

    # with open(csv_path, encoding='utf-8', errors='ignore') as f:
    with open(csv_path, encoding='utf-8', errors='ignore') as f:


        reader = csv.reader(f)

        # skip first line, as this is the header
        next(reader)

        for row in reader:
            # index = row[0]
            # stop_id = row[1]
            # name = row[3] + ", " + row[2]
            # lat = row[4]
            # lon = row[5]

            index = row[0]
            name = row[1] + ", " + row[2]
            lat = row[3]
            lon = row[4]
            stop_id = row[5]

            obj, created = Stop.objects.get_or_create(
                stop_id=stop_id,
                name=name,
                lat=lat,
                lon=lon,
            )

            if (created):
                print(stop_id, "created")
            else:
                print(stop_id, "already exists")


    print("Finished stops!")
    print()


def populate_routes(csv_path):

    with open(csv_path, encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)

        # skip first line, as this is the header
        next(reader)

        for row in reader:
            # index1 = row[0]
            # index2 = row[1]
            # route_id = row[2]
            # journey_pattern = str(row[3])
            # # headsign = row[4]

            # index = row[0]
            # route_id = row[1]
            # journey_pattern = row[2]

            route_id = row[0]
            journey_pattern = row[1]
            headsign = row[2]

            obj, created = Route.objects.get_or_create(
                route_id=route_id,
                journey_pattern=journey_pattern,
                headsign=headsign,
            )

            print(headsign)

            if created:
                print(route_id, "-", journey_pattern, "created")
            else:
                print(route_id, "already exists")

    print("Finished routes!")
    print()

def populate_route_stations(csv_path):
    missing_stops = set()
    missing_routes = set()

    with open(csv_path, encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)

        # skip first line, as this is the header
        next(reader)

        for row in reader:
            # index = row[0]
            # LineID = row[1]
            # JourneyPatternID = row[2]
            # Order = row[3]
            # StopID = row[4]
            # Headsign = row[5]
            # Name = row[7] + ", " + row[6]
            # Lat = row[8]
            # Lon = row[9]


            index = row[0]
            StopID = row[1]
            Runtime = str(row[2])
            Order = row[3]
            LineID = row[4]
            JourneyPatternID = int(float(row[5]))


            try:
                stop = Stop.objects.get(
                    stop_id=StopID,
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

                if created:
                    print(stop, route, "created")
                else:
                    print(stop, route, "already exists")
            except:
                print("Error!")

    print("Finished route stops!")
    print()

    return missing_stops, missing_routes


if __name__=="__main__":
    # stop_path = os.path.join(settings.DATA_PATH, 'static_data_eoghan/stops.csv')
    # route_path = os.path.join(settings.DATA_PATH, 'static_data_eoghan/lines.csv')
    # routestops_path = os.path.join(settings.DATA_PATH, 'static_data_eoghan/routestations3.csv')
    # routestops_path = os.path.join(settings.DATA_PATH, 'static_data/route_stops_all.csv')

    stop_path = os.path.join(settings.DATA_PATH, 'static_data3/stops.csv')
    route_path = os.path.join(settings.DATA_PATH, 'static_data3/routes_all(headsigns).csv')
    routestops_path = os.path.join(settings.DATA_PATH, 'static_data3/route_stops_all.csv')

    populate_stops(stop_path)
    populate_routes(route_path)
    populate_route_stations(routestops_path)


