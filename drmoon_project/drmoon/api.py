from tastypie.resources import ModelResource
from drmoon.models import NetworkGraph


class NetworkGraphResource(ModelResource):
    class Meta:
        queryset = NetworkGraph.objects.all()
        resource_name = 'networkgraph'
