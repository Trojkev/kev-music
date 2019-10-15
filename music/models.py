# -*- coding: utf-8 -*-
import uuid
from django.db import models
from account.models import State


class Album(models.Model):
    artist = models.CharField(max_length=60)
    album_title = models.CharField(max_length=30, unique = True)
    genre = models.CharField(max_length=20, null = True, default = 'Other')
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    album_logo = models.CharField(max_length=200, null=True, blank=True) # a link to the album_logo
    key = models.CharField(max_length = 255, default = uuid.uuid4, editable = False)
    date_modified = models.DateTimeField(auto_now = True)
    date_created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return '%s - %s' % (self.album_title, self.artist)


class Song(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=50, editable = True, unique = True)
    file_type = models.CharField(max_length=10, null = True, blank = True, default = ".mp3")
    is_favorite = models.BooleanField(default=False, editable = True)
    key = models.CharField(max_length = 255, default = uuid.uuid4, editable = False)
    date_modified = models.DateTimeField(auto_now = True)
    date_created = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return '%s%s' % (self.song_title, self.file_type)


class Artist(models.Model):
    name = models.CharField(max_length = 50)
    alias = models.CharField(max_length = 50)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    key = models.CharField(max_length = 255, default = uuid.uuid4, editable = False)
    date_modified = models.DateTimeField(auto_now = True)
    date_created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name
