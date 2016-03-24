from django.shortcuts import render
from django.views import generic
from . models import Song

# Create your views here


class Top100Page(generic.TemplateView):
    template_name = "top100.html"


class AddLyricsPage(generic.TemplateView):
    template_name = "add.html"


class SongDetailView(generic.DetailView):
    model = Song
    context_object_name = "song"
    extra_context = {}

    def render_to_response(self, context):
        return super(SongDetailView, self).render_to_response(context, content_type="text/html")

    def get_context_data(self, **kwargs):
        context = super(SongDetailView, self).get_context_data(**kwargs)
        return context
