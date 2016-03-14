from __future__ import unicode_literals
import uuid
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import datetime
# Create your models here.
# from artist.models import Singer, Lyricist, MusicDirector
from song.models import Song


@python_2_unicode_compatible
class Album(models.Model):
    # TODO: Define fields here
    name = models.CharField(max_length=100)
    slug = models.UUIDField(primary_key=True, editable=False)
    YEAR_CHOICES = []
    for r in range(1980, (datetime.datetime.now().year + 1)):
        YEAR_CHOICES.append((r, r))
    year = models.IntegerField(('year'),
                               choices=YEAR_CHOICES,
                               default=datetime.datetime.now().year, blank=True)
    # singers = models.ManyToManyField(Singer, related_name='singer')
    # lyricists = models.ManyToManyField(Lyricist, related_name='lyricist')
    # musicDirectors = models.ManyToManyField(MusicDirector, related_name='musicDirector')
    # genres = models.ForeignKey(Genre)
    songs = models.ManyToManyField(Song, related_name='Song', blank=True)

    class Meta:
        verbose_name = "Album"
        verbose_name_plural = "Albums"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = uuid.uuid4()
        return super(Album, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('')

    # TODO: Define custom methods here
