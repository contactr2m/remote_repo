from django.contrib import admin

# Register your models here.
from album.models import Album
# from artist.admin import SingerInline, LyricistInline, MusicDirectorInline
from song.admin import SongInline, GenreInline


# class AlbumInline(admin.TabularInline):
#     model = Song.album.through


class AlbumAdmin(admin.ModelAdmin):
    '''
        Admin View for AlbumInline
    '''
    list_display = ('name', 'year',)
    # list_filter = ('',)
    inlines = [  # GenreInline,
        # SingerInline,
        # LyricistInline,
        # MusicDirectorInline,
        SongInline,
    ]
    # raw_id_fields = ('',)
    readonly_fields = ('slug',)
    search_fields = ('name',)
    exclude = ('songs',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # call super method if object has no primary key
            super(AlbumAdmin, self).save_model(request, obj, form, change)
        else:
            pass  # don't actually save the parent instance

    def save_related(self, request, form, formsets, change):
        form.save_m2m()
        for formset in formsets:
            self.save_formset(request, form, formset, change=change)
        super(AlbumAdmin, self).save_model(request, form.instance, form, change)

admin.site.register(Album, AlbumAdmin)
