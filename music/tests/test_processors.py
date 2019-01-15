import pytest
from mixer.backend.django import mixer

from music.backend.processor import Processor

pytestmark = pytest.mark.django_db


class TestProcessor:
	"""
	This method tests the trx processors
	"""
	def test_register_account(self):
		"""
		This method tests the register_account processor
		@return: Account | None
		"""
		state = mixer.blend('account.State', name = 'Active')
		data = {
			'first_name': 'Kevin',
			'last_name': 'Macharia',
			'phone_number': '254717072416',
			'email': 'kelvinmacharia078@gmail.com',
			'date_of_birth': '2000-01-01',
			'gender': 'Male',
			'location': 'Nairobi'
			}
		account = Processor().register_account(data)
		assert account['status'] == 'success', 'Should return a success'
		
		data = {
			'first_name': '',
			'last_name': 'Macharia',
			'phone_number': '',
			'email': 'kelvinmacharia078@gmail.com',
			'date_of_birth': '2000-01-01',
			'gender': 'Male',
			'location': 'Nairobi'
			}
		account = Processor().register_account(data)
		assert account['message'] == 'Some fields are blank'
		
		data = {
			'first_name': 'Kev',
			'last_name': 12345,
			'phone_number': '254',
			'email': 'kelvinmacharia078@gmail.com',
			'date_of_birth': '2000',
			'gender': 'Male',
			'location': 'Nairobi'
			}
		account = Processor().register_account(data)
		assert account['message'] == 'Some entries are invalid'
		
		data = {
			'first_name': 'Kev',
			'last_name': 'Macharia',
			'phone_number': '254717072231',
			'email': 'kelvinmacharia078@gmail.com',
			'date_of_birth': '2000-01-01',
			'gender': 'Male',
			'location': state
			}
		account = Processor().register_account(data)
		assert account['message'] == 'Account not created'
		
	def test_create_album(self):
		mixer.blend('account.State', name = 'Active')
		payload = {
			'album_title': 'Divide',
			'artist': 'Ed Sheeran',
			'genre': 'RnB',
			}
		obj = Processor().create_album(payload)
		assert obj['status'] == 'success'

		payload = {
			'album_title': 'Divide',
			'artist': '',
			'genre': 'RnB',
			}
		obj = Processor().create_album(payload)
		assert obj['message'] == 'Some fields are empty'
		
	def test_create_song(self):
		state = mixer.blend('account.State', name = 'Active')
		album = mixer.blend('music.Album', state = state)
		payload = {
			'album_key': album.key,
			'song_title': 'Thinking Out Loud'
			}
		obj = Processor().create_song(payload)
		assert obj['status'] == 'success'
		
		payload = {
			'album_key': 'dnw',
			'song_title': 'Thinking Out Loud'
			}
		obj = Processor().create_song(payload)
		assert obj['message'] == 'Invalid Album entered'
		
		payload = {
			'album_key': album.key,
			'song_title': ''
			}
		obj = Processor().create_song(payload)
		assert obj['message'] == 'Some fields are empty.'
