from music.models import Song, Album
import logging

lgr = logging.getLogger(__name__)


class AlbumService(object):
	"""
	This class handles all the CRUD operations on the Album model. i.e :
		1. get_album(*args, **kwargs)
		2. create_album(**kwargs)
		3. filter_album(*args, **kwargs)
		4. update_album(key, **kwargs)
	"""
	
	@staticmethod
	def get_album(*args, **kwargs):
		"""
		This method returns an album object by the passed parameters or None if not found
		@param args: arguments passed to the method
		@param kwargs: key -> word arguments passed to this method
		@return: Album | None
		"""
		try:
			return Album.objects.get(*args, **kwargs)
		except Exception as e:
			lgr.error("get_album Exception: %s", e)
			return None
	
	@staticmethod
	def filter_album(*args, **kwargs):
		"""
		This method returns a queryset of the Album objects meeting the filtering criteria or None if not found
		@param args: arguments passed to the filter method
		@param kwargs: key -> word arguments passed to the filter method
		@return: Album Queryset | None
		"""
		try:
			return Album.objects.filter(*args, **kwargs)
		except Exception as e:
			lgr.error("filter_album Exception: %s", e)
			return None
	
	@staticmethod
	def create_album(**kwargs):
		"""
		This method creates an Album object with the provided parameters or None if not provided
		@param kwargs: key->word arguments passed to the create method
		@return: Album | None
		"""
		try:
			return Album.objects.create(**kwargs)
		except Exception as e:
			lgr.error("create_album Exception: %s", e)
			return None
	
	@staticmethod
	def update_album(key, **kwargs):
		"""
		This method updates the Album object with parameters provided or None if not
		@param key: the album key to be updated
		@param kwargs: key->word arguments passed to this method for update
		@return: Album | None
		"""
		try:
			record = AlbumService().get_album(key = key)
			for attr, value in kwargs.items():
				setattr(record, attr, value)
			record.save()
			record.refresh_from_db()
			return record
		except Exception as e:
			lgr.error("update_album error: %s", e)
			return None


class SongService(object):
	"""
	This class handles all the CRUD operations relating to the Song model i.e:
		1. get_song(*args, **kwargs)
		2. filter_song(*args, **kwargs)
		3. create_song(**kwargs)
		4. update_song(key, **kwargs)
	"""
	
	@staticmethod
	def get_song(*args, **kwargs):
		"""
		This method returns a Song object from the provided parameters or None if not found
		@param args: arguments passed to the get method
		@param kwargs: key->word arguments [passed to the filter method
		@return: Song | None
		"""
		try:
			return Song.objects.get(*args, **kwargs)
		except Exception as e:
			lgr.error("get_song Exception: %s", e)
			return None
	
	@staticmethod
	def filter_song(*args, **kwargs):
		"""
		This method returns a queryset of Song objects meeting the filter criteria or None if not found
		@param: args: Arguments passed to the filter method
		@param: kwargs: Key->Word arguments passed to the filter method
		@return: Song QuerySet | None
		"""
		try:
			return Song.objects.filter(*args, **kwargs)
		except Exception as e:
			lgr.error("filter_song Exception: %s", e)
			return None
	
	@staticmethod
	def create_song(**kwargs):
		"""
		This method creates a Song object with the provided parameters or None if not provided
		@param kwargs: Key->Word arguments passed to the create method
		@return: Song | None
		"""
		try:
			return Song.objects.create(**kwargs)
		except Exception as e:
			lgr.error("create_song Exception: %s", e)
			return None
	
	@staticmethod
	def update_song(key, **kwargs):
		"""
		This method updates the Song object or None if not found
		@param key: the Song object key to be updated
		@param kwargs: Key->Word arguments to be updated
		@return: Song | None
		"""
		try:
			record = SongService().get_song(key = key)
			for attr, value in kwargs.items():
				setattr(record, attr, value)
			record.save()
			record.refresh_from_db()
			return record
		except Exception as e:
			lgr.error("update_song Exception: %s", e)
			return None
