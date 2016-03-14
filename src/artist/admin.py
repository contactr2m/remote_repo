from django.contrib import admin

# Register your models here.

from artist.models import Singer, Lyricist, MusicDirector
from song.models import Song


class SingerInline(admin.TabularInline):
    model = Song.singers.through


class LyricistInline(admin.TabularInline):
    model = Song.lyricists.through


class MusicDirectorInline(admin.TabularInline):
    model = Song.musicDirectors.through


class SingerAdmin(admin.ModelAdmin):
    pass


class LyricistAdmin(admin.ModelAdmin):
    pass


class MusicDirectorAdmin(admin.ModelAdmin):
    pass

admin.site.register(Singer, SingerAdmin)
admin.site.register(Lyricist, LyricistAdmin)
admin.site.register(MusicDirector, MusicDirectorAdmin)
