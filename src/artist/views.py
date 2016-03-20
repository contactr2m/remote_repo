from django.shortcuts import render
from django.views import generic
from artist.models import Artist
from django.utils import timezone
# Create your views here.


class ArtistPage(generic.TemplateView):
    template_name = "artist.html"


class ArtistDetailView(generic.DetailView):
    model = Artist
    context_object_name = "artist"
    extra_context = {}

    def render_to_response(self, context):
        return super(ArtistDetailView, self).render_to_response(context, content_type="text/html")

    def get_context_data(self, **kwargs):
        context = super(ArtistDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
