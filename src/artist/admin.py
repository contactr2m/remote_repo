from django.contrib import admin

# Register your models here.

from artist.models import Artist
from core.admin import BaseAdmin


class ArtistAdmin(BaseAdmin):

    list_display = ('name',)
    search_fields = ['name', 'song__name']
    list_filter = ('listed',)

    # RelationsInline,
    inlines = []

    """"""
    fieldsets = [
        (None, {'fields': ['name', 'slug', 'listed']}),
        ('Users', {'fields': ['creator', 'last_editor']}),
    ]

    raw_id_fields = [
        'creator',
        'last_editor',
    ]

admin.site.register(Artist, ArtistAdmin)
