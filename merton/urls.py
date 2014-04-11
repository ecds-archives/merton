from django.conf.urls import patterns, include, url
from merton.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('merton/views',
	#Ordered according to navigation bar
    url(r'^$|^home/$|^merton/$', index),
    url(r'^contents/$', contents),
    url(r'^browse/(.*)$', browse),
    url(r'^credits/$', credits),
    url(r'^display/(.+)/$', display_page),
    url(r'^search/$', search),
    url(r'^quickview/(.+)/$', quickview),
    url(r'^imageview/(.+)/$', imageview),
)
