from django.contrib import admin

# Register your models here.

from artist.models import Artist
from song.models import Song


class ArtistInline(admin.TabularInline):
    model = Song.artist.through


class ArtistAdmin(admin.ModelAdmin):
    pass

admin.site.register(Artist, ArtistAdmin)
