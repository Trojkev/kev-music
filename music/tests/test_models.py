import pytest
from django.test import TestCase
from mixer.backend.django import mixer

from music.models import Album, Song

pytestmark = pytest.mark.django_db


class TestModels:
    """
    This class tests the Music app models
    """
    def test_album(self):
        """
        This method tests the Album model
        @return: Album object | None
        """
        state = mixer.blend('account.State', name = 'Active')
        obj = mixer.blend('music.Album', state = state)
        result = Album.objects.get(pk = obj.id)
        assert result is not None, "Should return an Album object"
        
    def test_song(self):
        """
        This method tests the Song model
        @return: Song object | None
        """
        state = mixer.blend('account.State', name = 'Active')
        obj = mixer.blend('music.Song', state = state)
        result = Song.objects.get(pk = obj.id)
        assert result is not None, "Should return a Song object"


class MusicModelsTests(TestCase):
    
    def test_object_returned(self):
        mixer.blend('music.Album', album_title = 'Divide', artist = 'Ed Sheeran')
        album_obj = Album.objects.get(pk = 1)
        expected_name = '%s - %s' % (album_obj.album_title, album_obj.artist)
        self.assertEquals(expected_name, unicode(album_obj))
    
        mixer.blend('music.Song', name = 'Thinking out Loud')
        song_obj = Song.objects.get(pk = 1)
        expected_name = '%s%s' % (song_obj.song_title, song_obj.file_type)
        self.assertEquals(expected_name, unicode(song_obj))
