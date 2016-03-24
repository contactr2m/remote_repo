# -*- coding: utf-8 -*-
import datetime
import django_filters
from django.utils.translation import ugettext as _
from artist.models import Artist
from django.db import models

ORDER_BY_FIELD = 'o'


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
