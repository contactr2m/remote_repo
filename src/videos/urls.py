from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^videos/$', views.VideoPage.as_view(), name='videos'),
]
