import django
import sys, os, csv

# ----- are these even necessary? ----- 
# change this to your own path if you are running the program
# project_path = "~Desktop/compsci/ResearchPracticum/DjangoSite/"

# sys.path.append(project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'DjangoSite.settings'
django.setup()

from bus.models import Stop


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
            print(index, stop_id, name, lat, lon)

            obj, created = Stop.objects.get_or_create(
                stop_id=row[1],
                name=row[2] + " - " + row[3],
                lat=row[4],
                lon=row[5],
            )


if __name__=="__main__":
    stop_path = "static_data/stops_all.csv"
    populate_stops(stop_path)
