from django.shortcuts import render
from django.views import generic
# Create your views here.


class VideoPage(generic.TemplateView):
    template_name = "videos.html"
