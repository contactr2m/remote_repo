from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^albums/$', views.AlbumsPage.as_view(), name='albums'),
    url(r'^(?P<pk>\d+)-(?P<slug>[-\w]+)/$', views.AlbumDetailView.as_view(), name='album-detail'),
    #url(r'^(?P<pk>\d+)/edit/$', views.AlbumEditView.as_view(), name='album-edit'),
    url(r'^$', views.AlbumListView.as_view(), name='album-list'),
]

