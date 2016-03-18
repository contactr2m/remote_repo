from __future__ import unicode_literals
import uuid
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from django.db import IntegrityError
# Create your models here.
from select_multiple_field.models import SelectMultipleField
from django.utils.translation import ugettext_lazy as _

@python_2_unicode_compatible
class Person(models.Model):
    # TODO: Define fields here
    name = models.CharField(max_length=50)
    birthDate = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At',)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Last Modified At',)
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
    # TODO: Define fields here
    slug = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Singer = 's'
    MusicDirector = 'm'
    Lyricist = 'l'
    ROLE_CHOICES = (
        (Singer, _('Singer')),
        (MusicDirector, _('MusicDirector')),
        (Lyricist, _('Lyricist')),
    )
    type = SelectMultipleField(choices=ROLE_CHOICES, max_length=3, default=Singer)

    class Meta:
        verbose_name = "Artist"
        verbose_name_plural = "Artists"
        unique_together = ("slug", "type", "name")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = uuid.uuid4()
        return super(Artist, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('')

    # TODO: Define custom methods here
