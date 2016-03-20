from django.shortcuts import render
from django.views import generic
from album.models import Album
from django.utils import timezone
# Create your views here.


class AlbumsPage(generic.TemplateView):
    template_name = "albums.html"


class AlbumDetailView(generic.DetailView):
    model = Album
    context_object_name = "album"
    extra_context = {}

    def render_to_response(self, context):
        return super(AlbumDetailView, self).render_to_response(context, content_type="text/html")

    def get_context_data(self, **kwargs):
        context = super(AlbumDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
