from __future__ import unicode_literals

from django.db import models
import uuid
from django.utils.encoding import python_2_unicode_compatible
from django_extensions.db.fields import AutoSlugField
from django.utils.translation import ugettext as _
from django.conf import settings
from .managers import SongManager
from django.core.urlresolvers import reverse
from core.util.custom_slug import unique_slugify
from core.models import TimeAuditModel
# Create your models here.


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
            #    super(Genre, self).save(*args, **kwargs)
            self.slug = uuid.uuid4()
        return super(Genre, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('')

    # TODO: Define custom methods here


@python_2_unicode_compatible
class Song(TimeAuditModel):
    #   Define fields here
    name = models.CharField(max_length=100, db_index=True)
    slug = AutoSlugField(populate_from='name', editable=True, blank=True, overwrite=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    artist = models.ForeignKey('artist.Artist', blank=True, null=True, related_name='song_artist')
    song_artists = models.ManyToManyField('artist.Artist', related_name='credited',
                                          through='SongArtists',
                                          blank=True)
    album = models.ForeignKey('album.Album', blank=True, null=True, related_name='song_album',
                              on_delete=models.SET_NULL)
    genres = models.ForeignKey(Genre, related_name='song_genre', blank=True, null=True)
    lyrics = models.TextField(max_length=500)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True,
                                null=True, related_name="song_creator",
                                on_delete=models.SET_NULL)
    last_editor = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True,
                                    null=True, related_name="song_last_editor",
                                    on_delete=models.SET_NULL)
    listed = models.BooleanField(verbose_name='Include in listings', default=True,
                                 help_text=_('Should this Song be shown on the default list?'))
    disable_editing = models.BooleanField(verbose_name='Disable Editing', default=False,
                                          help_text=_('Disable Editing. If verified by admin'))

    objects = SongManager()

    # Define custom methods here

    class Meta:
        verbose_name = "Song"
        verbose_name_plural = "Songs"
        ordering = ("-name",)

    def __str__(self):
        return self.name

    @property
    def classname(self):
        return self.__class__.__name__

    def save(self, *args, **kwargs):
        unique_slugify(self, self.name)
        return super(Song, self).save(*args, **kwargs)
        # return super(Song, self).save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse('songs:song-detail', kwargs={'pk': str(self.pk),
                                                    'slug': self.slug,
                                                    })

    def get_edit_url(self):
        return reverse("songs:song-edit", args=(self.pk,))

    def get_admin_url(self):
        return reverse("admin:song_change", args=(self.pk,))

    def get_song_artists(self):

        artists = []
        if self.song_artists.count() > 0:
            for song_artist in self.song_songartist.all():
                artists.append({'artist': song_artist.artist})
            return artists

        return artists

    def get_artist_display(self):
        artist_str = ''
        artists = self.get_song_artists()
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

                try:
                    artist_str = self.artist.name
                except:
                    artist_str = _('Unknown Artist')

        return artist_str


@python_2_unicode_compatible
class SongArtists(models.Model):
    artist = models.ForeignKey('artist.Artist', related_name='artist_songartist')
    song = models.ForeignKey(Song, related_name='song_songartist')

    class Meta:
        verbose_name = _('Artist (title credited)')
        verbose_name_plural = _('Artists (title credited)')

    def __str__(self):
        return '%s on %s' % (self.artist, self.song)
