from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^albums/$', views.AlbumsPage.as_view(), name='albums'),
]

