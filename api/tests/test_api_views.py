import pytest
from django.test import RequestFactory, TestCase
from mixer.backend.django import mixer

from api.views import PrimaryAPI

pytestmark = pytest.mark.django_db


class TestViews(TestCase):
	"""
	This class tests the api endpoints in PrimaryAPI class
	"""
	
	def setUp(self):
		"""
		Set up the functions to be run before each test case.

		Set up global states and types required throughout the tests.
		@return:
		@rtype:
		"""
		self.factory = RequestFactory()
		
	def test_accounts(self):
		data = {
			'offset': 10,
			'page_size': 100
			}
		request = self.factory.get('api/accounts/', data = data)
		result = PrimaryAPI().accounts(request)
		self.assertEquals(result.status_code, 200)
		
	def test_albums(self):
		data = {
			'offset': 10,
			'page_size': 100
			}
		request = self.factory.get('api/albums/', data = data)
		result = PrimaryAPI().albums(request)
		self.assertEquals(result.status_code, 200)
	
	def test_songs(self):
		data = {
			'offset': 10,
			'page_size': 100
			}
		request = self.factory.get('api/songs/', data = data)
		result = PrimaryAPI().songs(request)
		self.assertEquals(result.status_code, 200)
	
	def test_register_account(self):
		"""
		This method tests the register_account api endpoint
		"""
		mixer.blend('account.State', name = 'Active')
		data = {
			'first_name': 'Kevin',
			'last_name': 'Macharia',
			'phone_number': '254717072416',
			'email': 'kelvinmacharia078@gmail.com',
			'date_of_birth': '2000-01-01',
			'gender': 'Male',
			'location': 'Nairobi',
			'pin': ''
			}
		request = self.factory.post('api/register_account/', data = data)
		account = PrimaryAPI().register_account(request)
		self.assertEquals(account.status_code, 200)
	
	def test_create_album(self):
		"""
		This method tests the create_album api endpoint
		@return: status_code
		"""
		mixer.blend('account.State', name = 'Active')
		data = {
			'album_title': 'Divide',
			'artist': 'Ed Sheeran',
			'genre': 'RnB',
			}
		request = self.factory.post('api/create_album/', data = data)
		result = PrimaryAPI().create_album(request)
		self.assertEquals(result.status_code, 200)
		
		data = {
			'album_title': '',
			'artist': '',
			'genre': 'RnB',
			'album_logo': 'hfdjefihg'
			}
		request = self.factory.post('api/create_album/', data = data)
		result = PrimaryAPI().create_album(request)
		self.assertEquals(result.status_code, 400)
		
		data = {
			}
		self.factory.post('api/create_album/', data = data)
		result = PrimaryAPI().create_album(data)
		self.assertEquals(result.status_code, 500)
		
	def test_create_song(self):
		"""
		This method tests the create_song api endpoint
		@return: status_code
		"""
		state = mixer.blend('account.State', name = 'Active')
		album = mixer.blend('music.Album', album_title = 'Divide', state = state)
		
		data = {
			'album_key': album.key,
			'song_title': 'Shape of You'
			}
		request = self.factory.post('api/create_song/', data = data)
		result = PrimaryAPI().create_song(request)
		self.assertEquals(result.status_code, 200)

		data = {
			'album_key': 'key',
			'song_title': 'Shape of You'
			}
		request = self.factory.post('api/create_song/', data = data)
		result = PrimaryAPI().create_song(request)
		self.assertEquals(result.status_code, 400)
		
		data = {
			}
		result = PrimaryAPI().create_song(data)
		self.assertEquals(result.status_code, 500)
