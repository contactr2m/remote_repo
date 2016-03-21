from __future__ import unicode_literals
import uuid
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import datetime
from datetime import date
from datetime import timedelta
from django_extensions.db.fields import AutoSlugField
from django.utils.translation import ugettext as _
from django.conf import settings
from .managers import AlbumManager
from django.core.urlresolvers import reverse
from core.util.custom_slug import unique_slugify
import logging
from core.models import TimeAuditModel
from django.contrib.contenttypes.models import ContentType
# Create your models here.
logger = logging.getLogger("project")


@python_2_unicode_compatible
class Album(TimeAuditModel):
    # Define fields here
    name = models.CharField(max_length=100, db_index=True)
    slug = AutoSlugField(populate_from='name', editable=True, blank=True, overwrite=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    YEAR_CHOICES = []
    for r in range(1980, (datetime.datetime.now().year + 1)):
        YEAR_CHOICES.append((r, r))
    year = models.IntegerField(('year'),
                               choices=YEAR_CHOICES,
                               default=datetime.datetime.now().year, blank=True)
    songs = models.ManyToManyField('song.Song', related_name='albums', blank=True,
                                   through='AlbumSong')
    #   Image field
    releasedate = models.DateField(blank=True, null=True)
    TOTALTRACKS_CHOICES = ((x, x) for x in range(1, 301))
    totaltracks = models.IntegerField(verbose_name=_('Total Tracks'), blank=True,
                                      null=True, choices=TOTALTRACKS_CHOICES)
    DEFAULT_RELEASETYPE_CHOICES = ((_('General'), (
        ('album', _('Album')),
        ('single', _('Single')),)),)
    albumtype = models.CharField(verbose_name="Album type", max_length=24, blank=True,
                                 null=True, choices=DEFAULT_RELEASETYPE_CHOICES)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                                related_name="album_creator", on_delete=models.SET_NULL)
    last_editor = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                                    related_name="album_last_editor", on_delete=models.SET_NULL)
    album_artists = models.ManyToManyField('artist.Artist', through='AlbumArtists',
                                           related_name="album_albumartists", blank=True)

    objects = AlbumManager()

    # Define custom methods here

    @property
    def publish_date(self):
        # compatibility hack TODO: refactor all dependencies
        return datetime.utcnow()

    class Meta:
        verbose_name = "Album"
        verbose_name_plural = "Albums"
        ordering = ("-created_at",)

    def __str__(self):
        return self.name

    @property
    def classname(self):
        return self.__class__.__name__

    def is_active(self):
        now = date.today()
        try:
            if not self.releasedate:
                return True
            if self.releasedate <= now:
                return True
        except:
            pass
        return False

    @property
    def is_new(self):
        if self.releasedate and self.releasedate > (datetime.now() - timedelta(days=7)).date():
            return True
        return False

    def get_absolute_url(self):
        return reverse("albums:album-detail", kwargs={'pk': self.pk, 'slug': self.slug})

    def get_edit_url(self):
        return reverse("albums:album-edit", args=str(self.pk))

    def get_admin_url(self):
        info = (self._meta.app_label, self._meta.model_name)
        return reverse('admin:%s_%s_change' % info, args=str(self.pk,))

    def save(self, *args, **kwargs):
        unique_slugify(self, self.name)
        return super(Album, self).save(*args, **kwargs)

    def get_songs(self):
        from song.models import Song
        return Song.objects.filter(album=self)

    def get_media_indicator(self):
        media = self.get_media()
        indicator = []

        if self.totaltracks:
            for i in range(self.totaltracks):
                indicator.append(0)
            for m in media:
                try:
                    indicator[m.tracknumber - 1] = 3
                except Exception, e:
                    logger.info('Error'.format(e))
                    pass
        else:
            for m in media:
                indicator.append(2)
        return indicator

    def get_artist_display(self):
        artist_str = ''
        artists = self.get_artists()
        if len(artists) > 1:
            try:
                for artist in artists:
                    artist_str += artist['artist'].name
            except:
                artist_str = artists[0].name
        else:
            try:
                artist_str = artists[0].name
            except:
                artist_str = _('Unknown Artist')

        return artist_str

    def get_artists(self):
        artists = []
        if self.album_artists.count() > 0:
            for albumartist in self.album_albumartist_album.all():
                artists.append({'artist': albumartist.artist})
            return artists

        songs = self.get_songs()
        for song in songs:
            artists.append(song.artist)

        artists = list(set(artists))
        if len(artists) > 1:
            from artist.models import Artist
            a, c = Artist.objects.get_or_create(name="Various Artists")
            artists = [a]

        return artists


class AlbumArtists(models.Model):
    artist = models.ForeignKey('artist.Artist', related_name='album_albumartist_artist')
    album = models.ForeignKey('album.Album', related_name='album_albumartist_album')


class AlbumSong(models.Model):
    album = models.ForeignKey('album.Album')
    song = models.ForeignKey('song.Song')
