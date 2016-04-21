from django.shortcuts import render
from django.views import generic
from album.models import Album
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.conf import settings
from song.models import Song
from artist.models import Artist
from pure_pagination.mixins import PaginationMixin
from core.filter import AlbumFilter
import datetime
from datetime import timedelta


ALIBRARY_PAGINATE_BY = getattr(settings, 'ALIBRARY_PAGINATE_BY', (12, 24, 36, 120))
ALIBRARY_PAGINATE_BY_DEFAULT = getattr(settings, 'ALIBRARY_PAGINATE_BY_DEFAULT', 12)


ORDER_BY = [
    {
        'key': 'name',
        'name': _('Name')
    },
    {
        'key': 'releasedate',
        'name': _('Releasedate')
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


class AlbumListView(PaginationMixin, generic.ListView):
    object = Album
    paginate_by = ALIBRARY_PAGINATE_BY_DEFAULT
    model = Album

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
        context = super(AlbumListView, self).get_context_data(**kwargs)

        self.extra_context['filter'] = self.filter
        self.extra_context['special_filters'] = ['releasedate', ]
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
            #   qs = Release.objects.filter(Q(name__istartswith=q)\
            #   | Q(media_release__name__icontains=q)\
            #   | Q(media_release__artist__name__icontains=q)\
            #   | Q(label__name__icontains=q))\
            #   .distinct()
            qs = Album.objects.filter(name__icontains=q).distinct()
        else:
            qs = Album.objects.prefetch_related('song_album').all()

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
            qs = qs.filter(pk__in=(r.id for r in a.get_albums())).distinct()

            fa = Artist.objects.filter(slug=artist_filter)[0]
            f = {'item_type': 'artist', 'item': fa, 'label': _('Artist')}
            self.relation_filter.append(f)

        # filter by new flag
        new_filter = self.request.GET.get('new', None)
        if new_filter and new_filter.isnumeric() and int(new_filter) == 1:
            qs = qs.filter(releasedate__range=(datetime.datetime.now() - timedelta(days=14),
                                               datetime.datetime.now().date())).distinct()
            f = {'item_type': 'album', 'item': _('New Albums'), 'label': 'Filter'}
            self.relation_filter.append(f)

        # "extra-filters" (to provide some arbitary searches)
        extra_filter = self.request.GET.get('extra_filter', None)
        if extra_filter:
            # if extra_filter == 'no_cover':
            #     qs = qs.filter(main_image='').distinct()
            # if extra_filter == 'has_cover':
            #     qs = qs.exclude(main_image='').distinct()

            if extra_filter == 'possible_duplicates':
                from django.db.models import Count
                dupes = Album.objects.values('name').annotate(
                    Count('id')).order_by().filter(id__count__gt=1)
                qs = qs.filter(name__in=[item['name'] for item in dupes])
                if not order_by:
                    qs = qs.order_by('name')

        # apply filters
        self.filter = AlbumFilter(self.request.GET, queryset=qs)
        qs = self.filter.qs

        return qs
