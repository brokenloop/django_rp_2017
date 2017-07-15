from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^stops/$', views.stop_list),
    url(r'^stops/(?P<stop_id>[0-9]+)/$', views.stop_detail),
    url(r'^stops/common/(?P<stop_id1>[0-9]+)/(?P<stop_id2>[0-9]+)/$', views.route_stops_detail),
    url(r'^stops/(?P<stop_id>[0-9]+)/$', views.stop_detail),
    url(r'^time/$', views.time_estimate),
    url(r'^routes/$', views.route_list),
]
