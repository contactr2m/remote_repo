from __future__ import unicode_literals
import uuid
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from django.db import IntegrityError
# Create your models here.
from select_multiple_field.models import SelectMultipleField
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import UUIDField, AutoSlugField
from django.core.urlresolvers import reverse
from core.util.custom_slug import unique_slugify
from . managers import ArtistManager
from django.db.models import Q
from core.models import TimeAuditModel


@python_2_unicode_compatible
class Person(TimeAuditModel):
    # TODO: Define fields here
    name = models.CharField(max_length=50, db_index=True)
    birthDate = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "Persons"
        abstract = True

    def __str__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('')

    # TODO: Define custom methods here


class Artist(Person):
    #   Define fields here
    #   slug = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    slug = AutoSlugField(populate_from='name', editable=True, blank=True,
                         overwrite=True, db_index=True)
    Singer = 's'
    MusicDirector = 'm'
    Lyricist = 'l'
    ROLE_CHOICES = (
        (Singer, _('Singer')),
        (MusicDirector, _('MusicDirector')),
        (Lyricist, _('Lyricist')),
    )
    type = SelectMultipleField(choices=ROLE_CHOICES, max_length=3, default=Singer)
    bio = models.TextField(blank=True, null=True)
    #   Artist alias field, may be we need to create alias model too. low priority !
    #   Tagging field, low priority !
    #   User reversion app to control changes to module.
    #   http://django-reversion.readthedocs.org/en/latest/how-it-works.html
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True,
                                null=True, related_name="artists_creator",
                                on_delete=models.SET_NULL)
    last_editor = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True,
                                    null=True, related_name="artists_last_editor",
                                    on_delete=models.SET_NULL)
    listed = models.BooleanField(verbose_name='Include in listings', default=True,
                                 help_text=_('Should this Artist be shown on the default list?'))
    disable_editing = models.BooleanField(verbose_name='Disable Editing', default=False,
                                          help_text=_('Disable Editing. If verified by admin'))

    objects = ArtistManager()

    #   Define custom methods here

    class Meta:
        verbose_name = "Artist"
        verbose_name_plural = "Artists"
        #   unique_together = ("slug", "type", "name")
        ordering = ('name',)

    def __str__(self):
        return self.name

    @property
    def classname(self):
        return self.__class__.__name__

    def save(self, *args, **kwargs):
        # if not self.pk:
        #     self.uuid = uuid.uuid4()
        unique_slugify(self, self.name)
        return super(Artist, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return reverse('artist:artist-detail', kwargs={
            'pk': self.pk,
            'slug': self.slug,
        })

    def get_edit_url(self):
        return reverse("artist:artist-edit", args=(self.pk,))

    def get_admin_url(self):
        return reverse("admin:artist_change", args=(self.pk,))

    # TODO: Fix Me
    def get_song(self):
        from song.models import Song
        try:
            m = Song.objects.filter(Q(artist=self)).distinct()
            return m
        except Exception, e:
            return []
