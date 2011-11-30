from tastypie import fields
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource

from django.contrib.auth.models import User
from drmoon.models import NetworkGraph,UserProfile

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
	excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        allowed_methods = ['get']
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
    
    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(id=request.user.id)



class UserProfileResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = UserProfile.objects.all()
        resource_name = 'userprofile'
        allowed_methods = ['get']	
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
    
    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user)



class NetworkGraphResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = NetworkGraph.objects.all()
        resource_name = 'networkgraph'
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
	
    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user)
