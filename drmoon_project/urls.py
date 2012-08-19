import os

from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

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
    url(r'^networkgraphs/data/(?P<network_id>\d+)/$', 'drmoon.networkgraph_views.data')
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.SITE_ROOT,'drmoon','files')}),
    )
