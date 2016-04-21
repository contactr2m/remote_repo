from django.shortcuts import render
from django.views import generic
from django.utils.translation import ugettext as _
from django.conf import settings
from . models import Song
from artist.models import Artist
from album.models import Album
from pure_pagination.mixins import PaginationMixin
from core.filter import SongFilter


ALIBRARY_PAGINATE_BY = getattr(settings, 'ALIBRARY_PAGINATE_BY', (12, 24, 36, 120))
ALIBRARY_PAGINATE_BY_DEFAULT = getattr(settings, 'ALIBRARY_PAGINATE_BY_DEFAULT', 12)
ORDER_BY = [
    {
        'key': 'name',
        'name': _('Name')
    },
    {
        'key': 'artist__name',
        'name': _('Artist name')
    },
    {
        'key': 'updated',
        'name': _('Last modified')
    },
    {
        'key': 'created',
        'name': _('Creation date')
    },
]
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


class SongListView(PaginationMixin, generic.ListView):

    object = Song
    paginate_by = ALIBRARY_PAGINATE_BY_DEFAULT

    model = Song
    extra_context = {}

    def get_paginate_by(self, queryset):
        ipp = self.request.GET.get('ipp', None)
        if ipp:
            try:
                if int(ipp) in ALIBRARY_PAGINATE_BY:
                    return int(ipp)
            except Exception, e:
                pass

        return self.paginate_by

    def get_context_data(self, **kwargs):
        context = super(SongListView, self).get_context_data(**kwargs)

        self.extra_context['filter'] = self.filter
        self.extra_context['relation_filter'] = self.relation_filter
        self.extra_context['tagcloud'] = self.tagcloud
        # for the ordering-box
        self.extra_context['order_by'] = ORDER_BY

        # active tags

        self.extra_context['list_style'] = self.request.GET.get('list_style', 's')
        self.extra_context['get'] = self.request.GET
        context.update(self.extra_context)

        return context

    def get_queryset(self, **kwargs):
        kwargs = {}
        self.tagcloud = None
        q = self.request.GET.get('q', None)

        if q:
            #   qs = Media.objects.filter(Q(name__icontains=q)\
            #   | Q(release__name__icontains=q)\
            #   | Q(artist__name__icontains=q))\
            #   .distinct()
            qs = Song.objects.filter(name__icontains=q).distinct()
        else:
            qs = Song.objects.all()

        order_by = self.request.GET.get('order_by', 'created_at')
        direction = self.request.GET.get('direction', 'descending')

        if order_by and direction:
            if direction == 'descending':
                qs = qs.order_by('-%s' % order_by)
            else:
                qs = qs.order_by('%s' % order_by)

        # special relation filters
        self.relation_filter = []

        artist_filter = self.request.GET.get('artist', None)
        if artist_filter:
            a = Artist.objects.get(slug=artist_filter)
            qs = qs.filter(pk__in=(r.id for r in a.get_song())).distinct()

            fa = Artist.objects.filter(slug=artist_filter)[0]
            f = {'item_type': 'artist', 'item': fa, 'label': _('Artist')}
            self.relation_filter.append(f)

        album_filter = self.request.GET.get('album', None)
        if album_filter:
            qs = qs.filter(album__slug=album_filter).distinct()
            fa = Album.objects.filter(slug=album_filter)[0]
            f = {'item_type': 'album', 'item': fa, 'label': _('Album')}
            self.relation_filter.append(f)

        # apply filters
        self.filter = SongFilter(self.request.GET, queryset=qs)
        return qs
