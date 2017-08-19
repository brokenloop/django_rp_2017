from django.conf.urls import url
from . import views
from bus import views as bus_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^stops/$', bus_views.stop_list),
    url(r'^directions/$', views.get_directions),
]