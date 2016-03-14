from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^news/$', views.NewsPage.as_view(), name='news'),
]
