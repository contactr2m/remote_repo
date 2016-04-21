from django.shortcuts import (render, get_object_or_404, render_to_response)
from django.conf import settings
from django.views import generic
from django.db.models import Q
from django.utils.translation import ugettext as _
from django.utils import timezone
from pure_pagination.mixins import PaginationMixin
from artist.models import Artist
from album.models import Album
from song.models import Song
from core.filter import ArtistFilter
# Create your views here.
ALIBRARY_PAGINATE_BY = getattr(settings, 'ALIBRARY_PAGINATE_BY', (12, 24, 36, 120))
ALIBRARY_PAGINATE_BY_DEFAULT = getattr(settings, 'ALIBRARY_PAGINATE_BY_DEFAULT', 12)
ORDER_BY = [
    {
        'key': 'name',
        'name': _('Name')
    },
    {
        'key': 'updated_at',
        'name': _('Last modified')
    },
    {
        'key': 'created_at',
        'name': _('Creation date')
    },
]


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
        obj = kwargs.get('object', None)
        query1 = Q(song_album__artist=obj)
        query2 = Q(album_artists=obj)
        self.extra_context['m_contrib'] = Song.objects.filter(song_artists=obj)[0:48]
        self.extra_context['albums'] = Album.objects.filter(query1 | query2).distinct()[0:8]
        s_top = []
        # TODO: Votes not implemented yet.
        # song_top = Song.objects.filter(artist=obj,
        #                                votes__vote__gt=0).order_by('-votes__vote').distinct()
        song_top = Song.objects.filter(artist=obj)
        if song_top.count() > 0:
            song_top = song_top[0:10]
            for song in song_top:
                s_top.append(song)

        self.extra_context['s_top'] = s_top
        context.update(self.extra_context)
        return context


class ArtistListView(PaginationMixin, generic.ListView):

    #   context_object_name = "artist_list"
    #   template_name = "alibrary/release_list.html"

    object = Artist
    paginate_by = ALIBRARY_PAGINATE_BY_DEFAULT

    model = Album
    extra_context = {}

    def get_paginate_by(self, queryset):

        ipp = self.request.GET.get('ipp', None)
        if ipp:
            try:
                if int(ipp) in ALIBRARY_PAGINATE_BY:
                    return int(ipp)
            except Exception as e:
                pass

        return self.paginate_by

    def get_context_data(self, **kwargs):

        context = super(ArtistListView, self).get_context_data(**kwargs)

        self.extra_context['filter'] = self.filter
        self.extra_context['relation_filter'] = self.relation_filter
        #   self.extra_context['tagcloud'] = self.tagcloud
        # for the ordering-box
        self.extra_context['order_by'] = ORDER_BY

        # active tags

        self.extra_context['list_style'] = self.request.GET.get('list_style', 'l')

        self.extra_context['get'] = self.request.GET
        context.update(self.extra_context)

        return context

    def get_queryset(self, **kwargs):
        kwargs = {}
        self.tagcloud = None
        q = self.request.GET.get('q', None)

        if q:
            qs = Artist.objects.filter(name__icontains=q).distinct()
        else:
            # only display artists with tracks a.t.m.
            qs = Artist.objects.all().prefetch_related('song_artist')

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
            qs = qs.filter(song_album__artist__slug=artist_filter).distinct()
            fa = Artist.objects.filter(slug=artist_filter)[0]
            f = {'item_type': 'artist', 'item': fa, 'label': _('Artist')}
            self.relation_filter.append(f)

        # apply filters
        self.filter = ArtistFilter(self.request.GET, queryset=qs)
        qs = self.filter.qs

        # rebuild filter after applying tags
        # tagging / cloud generation

        return qs
