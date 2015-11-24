from django.conf.urls import patterns, include, url
from merton.views import *

urlpatterns = patterns('merton/views',
	#Ordered according to navigation bar
    url(r'^$|^home/$|^merton/$', index, name='index'),
    url(r'^about/$', about, name='about'),
    url(r'^contents/$', contents, name='contents'),
    url(r'^credits/$', credits, name='credits'),
    url(r'^display/(?P<doc_id>[^/]+)/$', display_page, name='display'),
    url(r'^search/$', search, name='search'),
    url(r'^download$', send_file, name='send_file'),
    url(r'^bibliography/$', bibliography, name='bibliography'),
    url(r'^browse/$', browse, name='browse'),
    url(r'^browse/(?P<category>.+?)/$', browse),
    url(r'^quickview/(?P<doc_id>[^/]+)/$', quickview),
    url(r'^imageview/(?P<image>[^/]+)/$', imageview, name='imageview'),
    url(r'^preface/$', preface, name='preface'),    
    url(r'^synopsis/$', synopsis, name='synopsis'),
    url(r'^register/$', register, name='register'),
    url(r'^facsimiles/$', facsimiles, name='facsimiles'),    
)
