from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^stops/$', views.stop_list),
    url(r'^stops/(?P<stop_id>[0-9]+)/$', views.stop_detail),
]
