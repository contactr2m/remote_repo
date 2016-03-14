from django.shortcuts import render
from django.views import generic
# Create your views here.


class NewsPage(generic.TemplateView):
    template_name = "news.html"
