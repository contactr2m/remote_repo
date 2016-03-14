from __future__ import unicode_literals
import uuid
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from django.db import IntegrityError
# Create your models here.


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


class Singer(Person):
    # TODO: Define fields here
    slug = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        verbose_name = "Singer"
        verbose_name_plural = "Singers"

    def __str__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('')

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = uuid.uuid4()
        return super(Singer, self).save(*args, **kwargs)
        # return super(Singer, self).save(*args, **kwargs)
    # TODO: Define custom methods here


class Lyricist(Person):
    # TODO: Define fields here
    slug = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        verbose_name = "Lyricist"
        verbose_name_plural = "Lyricists"

    def __str__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('')

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = uuid.uuid4()
        return super(Lyricist, self).save(*args, **kwargs)
        # return super(Lyricist, self).save(*args, **kwargs)
    # TODO: Define custom methods here


class MusicDirector(Person):
    # TODO: Define fields here
    slug = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        verbose_name = "MusicDirector"
        verbose_name_plural = "MusicDirectors"

    def __str__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('')

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = uuid.uuid4()
        return super(MusicDirector, self).save(*args, **kwargs)
        # return super(MusicDirector, self).save(*args, **kwargs)
    # TODO: Define custom methods here
