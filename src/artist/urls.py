from django.conf.urls import include, url
from django.conf import settings

from . import views

urlpatterns = [
    url(r'^artist/$', views.ArtistPage.as_view(), name='artist'),
]
