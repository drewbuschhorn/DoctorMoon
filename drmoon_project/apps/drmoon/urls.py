from django.conf.urls.defaults import *


urlpatterns = patterns("",
    url(r'^index$', 'drmoon.networkgraph_views.index'),
    url(r'^form$', 'drmoon.networkgraph_views.form'),
    url(r'^detail/(?P<network_id>\d+)/$', 'drmoon.networkgraph_views.details'),
    url(r'^data/(?P<network_id>\d+)/$', 'drmoon.networkgraph_views.data')
)
