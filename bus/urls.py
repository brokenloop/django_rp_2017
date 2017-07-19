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
]
