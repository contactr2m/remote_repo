# -*- coding: utf-8 -*-
import datetime
import django_filters
from django.utils.translation import ugettext as _
from artist.models import Artist
from song.models import Song
from album.models import Album
from django.db import models

ORDER_BY_FIELD = 'o'
DEFAULT_RELEASETYPE_CHOICES = ((_('General'), (
        ('album', _('Album')),
        ('single', _('Single')),)),)


class CharListFilter(django_filters.Filter):
    def filter(self, qs, value):
        if not value:
            return qs
        if isinstance(value, (list, tuple)):
            lookup = str(value[1])
            if not lookup:
                lookup = 'exact'
            value = value[0]
        else:
            values = value.split(',')
            lookup = self.lookup_type

        if value and values:

            if len(values) > 1:
                lookup = 'in'
                return qs.filter(**{'%s__%s' % (self.name, lookup): values})

            else:
                return qs.filter(**{'%s__%s' % (self.name, lookup): value})

        return qs


class DateRangeFilter(django_filters.Filter):

    range_start = None
    range_end = None

    def __init__(self, *args, **kwargs):
        super(DateRangeFilter, self).__init__(*args, **kwargs)

    @property
    def field(self):
        if not hasattr(self, '_field'):
            self._field = self.field_class(required=self.required,
                                           widget=self.widget, **self.extra)

        return self._field

    def filter(self, qs, value):

        range = value.split(':')
        range = range if len(range) == 2 else None

        if range:
            # try to extract the dates
            try:
                range_start = datetime.datetime.strptime(range[0], '%Y-%m-%d').date()
            except:
                range_start = None
            try:
                range_end = datetime.datetime.strptime(range[1], '%Y-%m-%d').date()
            except:
                range_end = None

            self.range_start = range_start
            self.range_end = range_end

            if range_start and range_end:
                return qs.filter(**{'%s__range' % self.name: (range_start, range_end)})

            if range_start and not range_end:
                return qs.filter(**{'%s__gte' % self.name: (range_start)})

            if not range_start and range_end:
                return qs.filter(**{'%s__lte' % self.name: (range_end)})

        return qs


class ArtistFilter(django_filters.FilterSet):
    type = CharListFilter(label=_("Artist type"))

    class Meta:
        model = Artist
        fields = [
            'artisttype',
        ]

    @property
    def filterlist(self):
        flist = []
        if not hasattr(self, '_filterlist'):
            for name, filter_ in self.filters.iteritems():
                ds = self.queryset.values_list(name, flat=False).order_by(name).annotate(
                    n=models.Count("pk", distinct=True)).distinct()
                filter_.entries = ds

                if ds not in flist:
                    flist.append(filter_)

            """
            add some custom queries
            """
            cf = {
                'label': 'Extra filters',
                'name': 'extra_filter',
                'entries': [
                    ['possible_duplicates', '', 'Duplicate detection'],
                ]
            }
            flist.append(cf)

            self._filterlist = flist

        return self._filterlist


class SongFilter(django_filters.FilterSet):

    class Meta:
        model = Song
        fields = [
            #   language ?
        ]

    @property
    def filterlist(self):
        flist = []
        if not hasattr(self, '_filterlist'):
            for name, filter_ in self.filters.iteritems():

                ds = self.queryset.values_list(name, flat=False).order_by(name).annotate(
                    n=models.Count("pk", distinct=True)).distinct()

                if ds not in flist:
                    flist.append(filter_)

            """
            add some custom queries
            """
            cf = {
                'label': 'Extra filters',
                'name': 'extra_filter',
                'entries': [
                    ['unassigned', '', 'Unassigned tracks'],
                    ['possible_duplicates', '', 'Duplicate detection'],
                    ['possible_duplicates_incl_artists', '', 'Duplicate (incl. Artist) detection'],
                ]
            }
            flist.append(cf)

            self._filterlist = flist

        return self._filterlist


class AlbumFilter(django_filters.FilterSet):
    releasetype = CharListFilter(label="Album type")
    releasedate = DateRangeFilter(label="Album date")

    class Meta:
        model = Album
        fields = ['releasedate', 'albumtype', ]

    @property
    def filterlist(self):

        flist = []

        if not hasattr(self, '_filterlist'):
            for name, filter_ in self.filters.iteritems():

                ds = self.queryset.values_list(name, flat=False).order_by(name).annotate(
                    n=models.Count("pk", distinct=True)).distinct()

                # TODO: extreme hackish...
                if name == 'releasetype_':
                    nd = []
                    for d in ds:
                        if d[0] == 'NULL':
                            pass
                        else:
                            print d[0]
                            if d[0] is not None:

                                for x in DEFAULT_RELEASETYPE_CHOICES:
                                    print x
                                    if x[0] == d[0]:
                                        print x[1]
                                        nd.append([d[0], d[1], x[1]])

                    filter_.entries = nd

                else:
                    filter_.entries = ds

                if ds not in flist:
                    flist.append(filter_)

            """
            add some custom queries
            """
            cf = {
                'label': 'Extra filters',
                'name': 'extra_filter',
                'entries': [
                    # ['no_cover', '', 'No cover'],
                    # ['has_cover', '', 'With cover'],
                    ['possible_duplicates', '', 'Duplicate detection'],
                ]
            }
            flist.append(cf)
            self._filterlist = flist
        return self._filterlist
