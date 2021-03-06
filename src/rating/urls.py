from django.conf.urls import *

from rating import views

urlpatterns = patterns('',
                       url(r'^(?P<content_type>[\w.]+)/(?P<object_id>\d+)/(?P<vote>-?\d{1})/$',
                           views.vote, name='vote'),
                       url(r'^(?P<content_type>[\w.]+)/(?P<object_id>\d+)/$',
                           views.vote, name='vote'),
                       )
