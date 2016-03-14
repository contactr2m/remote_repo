from __future__ import unicode_literals

from django.db import models
from artist.models import Singer, Lyricist, MusicDirector
import uuid
from django.utils.encoding import python_2_unicode_compatible
# Create your models here.


class TimeAuditModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At',)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Last Modified At',)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Genre(models.Model):
    # TODO: Define fields here
    name = models.CharField(max_length=50)
    slug = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
           # super(Genre, self).save(*args, **kwargs)
            self.slug = uuid.uuid4()
        return super(Genre, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('')

    # TODO: Define custom methods here


@python_2_unicode_compatible
class Song(TimeAuditModel):
    # TODO: Define fields here
    name = models.CharField(max_length=100)
    slug = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    singers = models.ManyToManyField(Singer, related_name='singer', blank=True)
    genres = models.ForeignKey(Genre, related_name='genre', blank=True, null=True)
    lyricists = models.ManyToManyField(Lyricist, related_name='lyricist', blank=True)
    musicDirectors = models.ManyToManyField(MusicDirector, related_name='musdicDirector', blank=True)
    lyrics = models.TextField(max_length=500)

    class Meta:
        verbose_name = "Song"
        verbose_name_plural = "Songs"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk is not None:
            self.slug = uuid.uuid4()
        return super(Song, self).save(*args, **kwargs)
        # return super(Song, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('')

    # TODO: Define custom methods here
