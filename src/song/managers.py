from django.db.models.query import QuerySet


class SongQuerySet(QuerySet):

    def listed(self):
        return self.filter(listed=True, priority__gt=0)

SongManager = SongQuerySet.as_manager
