from django.shortcuts import render
from django.views import generic
# Create your views here.


class AlbumsPage(generic.TemplateView):
    template_name = "albums.html"
