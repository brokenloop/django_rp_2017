from django.db import models


class Stop(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    name = models.CharField(max_length=250)
    stop_id = models.IntegerField()

    def __str__(self):
        return self.name


# class Route(models.Model):
#     route_id = models.IntegerField()
#     pattern_id = models.IntegerField()
#     direction = models.CharField(max_length=120)
#
#
# class RouteStation(models.Model):
#     stop = models.Foreignkey(Stop, on_delete=models.CASCADE)
#     route = models.Foreignkey(Route, on_delete=models.CASCADE)
#     order = models.IntegerField()
#
#
# class Timetable(models.Model):
#     route = models.ForeignKey(Route, on_delete=models.CASCADE)
#     time = models.