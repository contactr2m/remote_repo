from django.db.models.query import QuerySet
from datetime import datetime
from django.db.models import Q


class AlbumQuerySet(QuerySet):

    def active(self):
        now = datetime.now()
        return self.filter(
                Q(publish_date__isnull=True) |
                Q(publish_date__lte=now)
                )

AlbumManager = AlbumQuerySet.as_manager
