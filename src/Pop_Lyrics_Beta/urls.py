from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import profiles.urls
import videos.urls
import album.urls
import artist.urls
import song.urls
import news.urls
from . import views

urlpatterns = [
    url(r'^$', views.HomePage.as_view(), name='home'),
    url(r'^about/$', views.AboutPage.as_view(), name='about'),
    url(r'^users/', include(profiles.urls, namespace='profiles')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^', include(videos.urls, namespace='videos')),
    url(r'^', include(album.urls, namespace='albums')),
    url(r'^', include(artist.urls, namespace='artist')),
    url(r'^', include(news.urls, namespace='news')),
    url(r'^', include(song.urls, namespace='songs')),
]

# User-uploaded files like profile pics need to be served in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
