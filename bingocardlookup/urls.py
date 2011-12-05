from django.conf.urls.defaults import patterns, include, url
import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bingocardlookup.views.home', name='home'),
    # url(r'^bingocardlookup/', include('bingocardlookup.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    (r'^bingocardlookup/$', 'lookupapp.views.enter'),
    (r'^bingocardlookup/openid/', include('django_openid_auth.urls')),
    (r'^bingocardlookup/enter/$', 'lookupapp.views.enter'),
    (r'^bingocardlookup/decode/$', 'lookupapp.views.decode'),
    (r'^bingocardlookup/logout/$', 'lookupapp.views.logout'), 
    (r'^bingocardlookup/editcard/$', 'lookupapp.views.editcard'),   
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

#this is only for development...
urlpatterns += staticfiles_urlpatterns()
