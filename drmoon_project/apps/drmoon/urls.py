from django.conf.urls.defaults import *


urlpatterns = patterns("",
    url(r'^index$', 'drmoon.networkgraph_views.index',name='networkgraphs_index'),
    url(r'^form$', 'drmoon.networkgraph_views.form',name='networkgraphs_form'),
    url(r'^detail/(?P<network_id>\d+)/$', 'drmoon.networkgraph_views.details',name='networkgraphs_detail'),
    url(r'^data/(?P<network_id>\d+)/$', 'drmoon.networkgraph_views.data',name='networkgraphs_data')
)
