from django.contrib import admin

# Register your models here.
from song.models import Song, Genre
from artist.admin import ArtistInline
from album.models import Album


class GenreInline(admin.StackedInline):
    model = Genre


class GenreAdmin(admin.ModelAdmin):
    pass

    # def save_model(self, request, obj, form, change):
    #     if not obj.pk:  # call super method if object has no primary key
    #         super(GenreAdmin, self).save_model(request, obj, form, change)
    #     else:
    #         pass


admin.site.register(Genre, GenreAdmin)


class SongInline(admin.TabularInline):
    '''
          Tabular Inline View for Song
    '''
    model = Album.songs.through
    # # min_num = 3
    # max_num = 20
    # extra = 1
    # # raw_id_fields = (,)


class SongAdmin(admin.ModelAdmin):
    '''
        Admin View for AlbumInline
    '''
    list_display = ('name', 'genres',)
    # list_filter = ('',)
    inlines = [
                ArtistInline,
               ]
    # raw_id_fields = ('genres',)
    readonly_fields = ('slug',)
    search_fields = ('name',)
    exclude = ('artist',)

    # def save_model(self, request, obj, form, change):
    #     if not obj.pk:  # call super method if object has no primary key
    #         super(SongAdmin, self).save_model(request, obj, form, change)
    #     else:
    #         print("primary key is %s" % obj.pk)
    #         pass  # don't actually save the parent instance

    # def save_related(self, request, form, formsets, change):
    #     form.save_m2m()
    #     for formset in formsets:
    #         self.save_formset(request, form, formset, change=change)
    #     super(SongAdmin, self).save_model(request, form.instance, form, change)


admin.site.register(Song, SongAdmin)
