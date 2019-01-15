from mixer.backend.django import mixer
import pytest
from music.backend.backend_services import AlbumService, SongService

pytestmark = pytest.mark.django_db


class TestAlbumService:
	"""
	This class tests the AlbumService methods. i.e:
		1. test_get_album()
		2. test_filter_album()
		3. test_create_album()
		4. test_update_album()
	"""
	def test_get_album(self):
		state = mixer.blend('account.State', name = 'Active')
		obj = mixer.blend('music.Album', album_title = 'Divide', state = state)
		result = AlbumService().get_album(pk = obj.id)
		assert result is not None, 'Should return an Album object'
		
		result = AlbumService().get_album(pk = 2)
		assert result is None, 'Should return None'
	
	def test_filter_album(self):
		state = mixer.blend('account.State', name = 'Active')
		obj = mixer.cycle(2).blend('music.Album', album_title = 'Summer of 69', state = state)
		result = AlbumService().filter_album(state = state)
		assert len(obj) == len(result), 'Should return two records'
		
		result = AlbumService().filter_album(abcd = 'efg')
		assert result is None, 'Should return None'
		
	def test_create_album(self):
		state = mixer.blend('account.State', name = 'Active')
		data = {
			'state': state,
			'album_title': 'Summer of 69',
			'artist': 'Bryan Adams',
			'genre': 'Rock'
			}
		result = AlbumService().create_album(**data)
		assert result is not None, 'Should create an Album object'
		
		data = {
			'album_name': 'Summer of 69',
			'artist': 'Bryan Adams',
			'genre': 'Rock'
			}
		result = AlbumService().create_album(**data)
		assert result is None, 'Should return None'
		
	def test_update_album(self):
		state = mixer.blend('account.State', name = 'Active')
		obj = mixer.blend('music.Album', artist = 'Chris Daughtry', state = state)
		result = AlbumService().update_album(key = obj.key, album_title = 'Crawling Back')
		assert result.album_title == 'Crawling Back', 'Should update obj with a new album_title'
		
		result = AlbumService().update_album(key = 'obj.key', album_title = 'Crawling Back')
		assert result is None, 'Should return None'


class TestSongService:
	"""
	This class tests all the CRUD operations for the Song model. i.e:
		1. test_get_song()
		2. test_filter_song()
		3. test_create_song()
		4. test_update_song()
	"""
	
	def test_get_song(self):
		state = mixer.blend('account.State', name = 'Active')
		obj = mixer.blend('music.Song', state = state)
		result = SongService().get_song(pk = obj.id)
		assert result is not None, 'Should return a Song object'
		
		result = SongService().get_song(abs = 'dhgt')
		assert result is None, 'Should return None'
		
	def test_filter_song(self):
		state = mixer.blend('account.State', name = 'Active')
		obj = mixer.cycle(2).blend('music.Song', song_title = 'Sandstorm', state = state)
		result = SongService().filter_song(song_title = 'Sandstorm')
		assert len(result) == len(obj), 'Should return two Song records'
		
		result = SongService().filter_song(song = 'Sandstorm')
		assert result is None, 'Should return None'
		
	def test_create_song(self):
		state = mixer.blend('account.State', name = 'Active')
		album = mixer.blend('music.Album', state = state)
		data = {
			'state': state,
			'album': album,
			'song_title': 'Sandstorm',
			'file_type': '.mp3',
			}
		result = SongService().create_song(**data)
		assert result is not None, 'Should create a Song object'
		
		data = {
			'album': album,
			'title': 'Sandstorm',
			'file_type': '.mp3',
			}
		result = SongService().create_song(**data)
		assert result is None, 'Should return None'
		
	def test_update_song(self):
		state = mixer.blend('account.State', name = 'Active')
		obj = mixer.blend('music.Song', song_title = 'Sandstorm', state = state)
		result = SongService().update_song(obj.key, song_title = 'Lego House')
		record = SongService().get_song(id = obj.id)
		assert record.song_title == 'Lego House', 'Should update Song record with a new Title'
		
		obj = mixer.blend('music.Song', song_title = 'Sandstorm')
		result = SongService().update_song(obj.id, song_title = 'Lego House')
		assert result is None, 'Should return None'
