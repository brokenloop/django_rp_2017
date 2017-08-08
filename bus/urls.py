from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^stops/$', views.stop_list),
    url(r'^stops/(?P<stop_id>[0-9]+)/$', views.stop_detail),
    url(r'^stops/common/(?P<origin>[0-9]+)/(?P<destination>[0-9]+)/$', views.common_routes),
    url(r'^stops/(?P<stop_id>[0-9]+)/$', views.stop_detail),
    url(r'^time/$', views.time_estimate),
    url(r'^routes/$', views.route_list),
    url(r'^routes/stops/(?P<route_id>[a-zA-Z0-9]+)/(?P<journey_pattern>[a-zA-Z0-9]+)/$', views.route_stops),
    url(r'^routes/stops/(?P<route_id>[a-zA-Z0-9]+)/(?P<journey_pattern>[a-zA-Z0-9]+)/(?P<origin>[0-9]+)/'
        r'(?P<destination>[0-9]+)/$', views.middle_stops),
    url(r'^stops/accessible/$', views.accessible_stops),
    url(r'^routes/(?P<route_id>[a-zA-Z0-9]+)/$', views.route_patterns),
    url(r'^cookie/$', views.cookie),
    url(r'^routes/stops/(?P<route_id>[a-zA-Z0-9]+)/(?P<journey_pattern>[a-zA-Z0-9]+)/(?P<origin>[0-9]+)/$', views.origin_to_end),
]
