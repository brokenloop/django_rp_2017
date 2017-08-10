from django.db import models


class Stop(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    name = models.CharField(max_length=250, blank=True, default="None")
    stop_id = models.IntegerField(unique=True)

    def __str__(self):
        return self.name + ", " + str(self.stop_id)


class Route(models.Model):
    route_id = models.CharField(max_length=20)
    journey_pattern = models.CharField(max_length=20)
    headsign = models.CharField(max_length=40)
    stops = models.ManyToManyField(Stop, through="RouteStation")

    class Meta:
        unique_together = ('route_id', 'journey_pattern')

    def __str__(self):
        return str(self.route_id) + " " + str(self.headsign)


class RouteStation(models.Model):
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    order = models.IntegerField()

    class Meta:
        unique_together = ('stop', 'route')

    def __str__(self):
        return str(self.stop) + " " + str(self.order)


class Timetable(models.Model):
    day = models.CharField(max_length=10)
    route_id = models.CharField(max_length=20)
    departure = models.CharField(max_length=5)
    # direction = models.CharField(max_length=250, blank=True, default="None")
    # route = models.ForeignKey(Route, on_delete=models.CASCADE)
    journey_pattern = models.CharField(max_length=4)
    # stopheadsign = models.CharField(max_length=100)

    def __str__(self):
        return str(self.route_id) + " - " + str(self.journey_pattern) + " - " + str(self.departure)


                # class Timetable(models.Model):
#     route = models.ForeignKey(Route, on_delete=models.CASCADE)
#     time = models.