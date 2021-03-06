from django.contrib import admin

# Register your models here.
from song.models import Song, Genre, SongArtists
from album.models import Album
from core.admin import BaseAdmin


class GenreInline(admin.StackedInline):
    model = Genre


class GenreAdmin(admin.ModelAdmin):
    pass


admin.site.register(Genre, GenreAdmin)


class SongInline(admin.TabularInline):
    '''
          Tabular Inline View for Song
    '''
    model = Song
    exclude = ['slug', 'lyrics', 'creator']
    readonly_fields = ['artist', ]
    extra = 0


class AlbumSongSongInline(admin.TabularInline):
    model = Song
    extra = 1


class SongAlbumInline(admin.TabularInline):
    model = Album.songs.through
    extra = 1
    raw_id_fields = ['album', ]


class SongArtistsInline(admin.TabularInline):
    model = SongArtists
    extra = 2
    fieldsets = [
        (None, {'fields': ['artist']}),
    ]
    raw_id_fields = ['artist', ]


class SongAdmin(BaseAdmin):

    list_display = ('name', 'created_at', 'release_link', 'artist', )
    search_fields = ['artist__name', 'album__name', 'name']
    list_filter = ()

    inlines = [SongAlbumInline, SongArtistsInline]

    readonly_fields = [
        'slug',
        'uuid',
        'release_link',
    ]

    date_hierarchy = 'created_at'

    fieldsets = [
        (None, {'fields':
                ['name', 'slug', 'uuid', ('album', 'release_link',), 'artist', 'genres']
                }),

        ('Users', {'fields': ['creator', 'last_editor']}),
        ('Text', {'fields': ['lyrics', ]}),

    ]

    raw_id_fields = [
        'creator',
        'last_editor',
        'album',
        'artist',
    ]


admin.site.register(Song, SongAdmin)
