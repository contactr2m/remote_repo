from django.shortcuts import render
from django.views import generic


# Create your views here.
class Top100Page(generic.TemplateView):
    template_name = "top100.html"


class AddLyricsPage(generic.TemplateView):
    template_name = "add.html"
