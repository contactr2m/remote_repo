from django.shortcuts import render
from django.views import generic
# Create your views here.


class ArtistPage(generic.TemplateView):
    template_name = "artist.html"
