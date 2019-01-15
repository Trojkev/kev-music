from django.contrib.auth.models import User
from django.contrib.auth import hashers

from account.backend.services import StateService, AccountService
from music.backend.backend_services import AlbumService, SongService
import logging

from music.backend.validators import Validator as v

lgr = logging.getLogger(__name__)


class Processor(object):
	"""
	This class contains all the processors for the music app
	"""
	@staticmethod
	def response(message, status = 'failed', data = None):
		return {
			"status": str(status).lower(),
			"message": message,
			"data": data
			}
	
	@staticmethod
	def register_account(payload):
		"""
		This method registers an account using the passed in parameters
		@param payload:
		@return:
		"""
		try:
			first_name = payload.get('first_name', '')
			last_name = payload.get('last_name', '')
			phone_number = payload.get('phone_number', '')
			email = payload.get('email', '')
			date_of_birth = payload.get('date_of_birth', '')
			gender = payload.get('gender', '')
			pin = payload.get('pin', '')
			location = payload.get('location', '')
			
			if first_name != '' and phone_number != '' and date_of_birth != '' and email != '':
				if v.validate_email(email) \
						and v.validate_phone_number(phone_number) \
						and v.validate_date(str(date_of_birth)) \
						and v.validate_name(first_name) \
						and v.validate_name(last_name):
					
					pin_hash = hashers.make_password(pin)
					user = User.objects.create_user(phone_number, pin_hash)
					if user is None:
						raise Exception('User Not Created')
					user.email = email
					user.first_name = first_name
					user.last_name = last_name
					user.save()
					
					account = AccountService().get(phone_number = phone_number)
					if account is None:
						state = StateService().get(name = 'Active')
						account = AccountService().create(
								user = user,
								state = state,
								phone_number = phone_number,
								first_name = first_name,
								last_name = last_name,
								email = email,
								gender = gender,
								date_of_birth = date_of_birth,
								location = location,
								pin_hash = pin_hash
								)
						if account is not None:
							return Processor().response(
									status = 'success',
									message = 'Account registered successfully',
									data = account
									)
						return Processor().response(message = 'Account not created')
				return Processor().response(
						message = 'Some entries are invalid',
						data = {
							'email': email,
							'phone_number': phone_number,
							'date_of_birth': date_of_birth,
							'first_name': first_name,
							'last_name': last_name
							}
						)
			return Processor().response(message = 'Some fields are blank')
			
		except Exception as e:
			lgr.error('register_account Exception: %s', e)
			return Processor().response(
					message = 'register_account Failed'
					)
	
	@staticmethod
	def create_album(payload):
		"""
		This method creates a new album
		@param payload: parameters for creating an Album
		@return: Album | None
		"""
		try:
			album_title = payload.get('album_title', '')
			artist = payload.get('artist', '')
			genre = payload.get('genre', '')
			album_logo = payload.get('album_logo', '')
			
			if album_title != "" and artist != "":
				state = StateService().get(name = 'Active')
				if state is None:
					raise Exception('State is None')
				data = {
					"state": state,
					"album_title": album_title,
					"artist": artist,
					"genre": genre,
					"album_logo": album_logo
					}
				album = AlbumService().create_album(**data)
				if album is not None:
					return Processor.response(
							status = 'success',
							message = 'Album created successfully',
							data = album
							)
				else:
					return Processor.response(message = "Album not created")
			else:
				return Processor.response(message = "Some fields are empty")
		except Exception as e:
			lgr.error("create_album Exception: %s", e)
			return Processor().response(message = 'create_album_failed')
		
	@staticmethod
	def create_song(payload):
		"""
		This method creates a new song or None
		@param payload: the parameters needed to create a song object
		@return: Song | None
		"""
		try:
			album_key = payload.get("album_key", '')
			song_title = payload.get("song_title", '')
			
			if album_key != "" and song_title != "":
				album = AlbumService().get_album(key = album_key)
				if album is not None:
					state = StateService().get(name = 'Active')
					data = {
						"state": state,
						"album": album,
						"song_title": song_title
						}
					song = SongService().create_song(**data)
					if song is not None:
						return Processor().response(
								status = 'success',
								message = 'Song created successfully',
								data = song.song_title
								)
					return Processor().response(message = 'Song not created')
				else:
					return Processor().response(message = 'Invalid Album entered')
			else:
				return Processor().response(message = 'Some fields are empty.')
			
		except Exception as e:
			lgr.error("create_song Exception: %s", e)
			return None
