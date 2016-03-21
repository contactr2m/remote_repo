from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^add/$', views.AddLyricsPage.as_view(), name='add'),
    url(r'^top100/$', views.Top100Page.as_view(), name='top100'),
    url(r'^(?P<pk>\d+)-(?P<slug>[-\w]+)/$', views.SongDetailView.as_view(), name='song-detail'),
]
