from django.conf.urls import patterns, include, url
from merton.views import *

urlpatterns = patterns('merton/views',
	#Ordered according to navigation bar
    url(r'^$|^home/$|^merton/$', index, name='index'),
    url(r'^about/$', about, name='about'),
    url(r'^contents/$', contents, name='contents'),
    url(r'^credits/$', credits, name='credits'),
    url(r'^display/(.+)/$', display_page, name='display'),
    url(r'^search/$', search, name='search'),
    url(r'^download$', send_file, name='send_file'),

)
