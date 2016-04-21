from django.contrib import admin
from django.utils.translation import ugettext as _
from django.core import urlresolvers
# Register your models here.
from album.models import AlbumArtists, AlbumSong, Album
from song.admin import SongInline, AlbumSongSongInline
from core.admin import BaseAdmin


class AlbumArtistsInline(admin.TabularInline):
    model = AlbumArtists
    extra = 2
    fieldsets = [
        (None, {'fields': ['artist']}),
    ]
    raw_id_fields = ['artist', ]


class AlbumSongInline(admin.TabularInline):
    model = AlbumSong
    extra = 1
    inlines = [AlbumSongSongInline]


class AlbumAdmin(BaseAdmin):

    list_display = (
        #   'image_display',
        #   'name',
        'info_display',
        'meta_display',
        #   'catalognumber',
    )

    list_display_links = [
        #   'catalognumber',
    ]

    search_fields = [
        'name',
        #   'catalognumber',
        #   'label__name',
    ]

    list_filter = ('albumtype',)
    date_hierarchy = 'created_at'

    inlines = [
        AlbumArtistsInline,
        SongInline
    ]
    readonly_fields = ['slug']  # 'license', 'd_tags']

    raw_id_fields = [
        #   'label',
        #   'owner',
        'creator',
        'last_editor',
        #   'publisher',
    ]

    fieldsets = [
        (None, {
            'fields': ['name', 'slug', ('releasedate'), ('albumtype')]
        }),
        ('Users', {'fields': ['creator', 'last_editor']}),
    ]

    def info_display(self, obj):

        tpl = u"""<p>
        <strong><a href="{object_url}">{object_name}</strong></a><br>
        by: {artist_name}<br>
        </p>""".format(
            object_url= urlresolvers.reverse('admin:album_album_change', args=(obj.pk,)), # if obj.label else '#',
            object_name=obj.name[0:40],
            artist_name=obj.get_artist_display(),
            #   label_url=urlresolvers.reverse('admin:alibrary_label_change', args=(obj.label.pk,)) if obj.label else '#',
            #   label_name=obj.label,
        )
        return tpl

    info_display.short_description = _('Album')
    info_display.allow_tags = True

    def meta_display(self, obj):

        tpl = """<p>
        <strong>{releasedate}</strong><br>
        {type}<br>
        {num_tracks} Tracks<br>
        </p>""".format(
            releasedate=obj.releasedate,
            type=obj.get_albumtype_display(),
            num_tracks=obj.get_songs().count(),
        )
        return tpl

    meta_display.short_description = _('Metadata')
    meta_display.allow_tags = True


admin.site.register(Album, AlbumAdmin)
