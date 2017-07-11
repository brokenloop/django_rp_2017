from django.contrib import admin

# Register your models here.
from .models import Stop, Route, RouteStation

admin.site.register(Stop)
admin.site.register(Route)
admin.site.register(RouteStation)