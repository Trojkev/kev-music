# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Album, Song


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('artist', 'album_title', 'genre', 'album_logo', 'state', 'date_created')
    search_fields = ('artist', 'album_title', 'state__name')
admin.site.register(Album, AlbumAdmin)


class SongAdmin(admin.ModelAdmin):
    list_display = ('song_title', 'album', 'file_type', 'state', 'date_created')
    search_fields = ('song_title', 'album__album_title', 'file_type', 'state__name')

admin.site.register(Song, SongAdmin)
