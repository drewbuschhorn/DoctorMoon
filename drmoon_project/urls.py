from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from tastypie.api import Api
from drmoon.api import NetworkGraphResource, UserProfileResource,UserResource
v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(NetworkGraphResource())
v1_api.register(UserProfileResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'drmoon_project.views.home', name='home'),
    # url(r'^drmoon_project/', include('drmoon_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^accounts/$','django.contrib.auth.views.login'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    url(r'^accounts/registration/$', 'drmoon.registration_views.register'),

    url(r'^networkgraphs/index$', 'drmoon.networkgraph_views.index'),
    url(r'^networkgraphs/form$', 'drmoon.networkgraph_views.form'),
    url(r'^networkgraphs/detail/(?P<network_id>\d+)/$', 'drmoon.networkgraph_views.details'),
    url(r'^networkgraphs/data/(?P<network_id>\d+)/$', 'drmoon.networkgraph_views.data'),
    url(r'^api/',include(v1_api.urls))
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/dbuschho/Desktop/drmoon_project/drmoon/files'}),
    )
