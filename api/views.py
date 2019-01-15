# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import logging

from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from account.backend.services import AccountService
from api.backend.decorators import enable_spa
from music.backend.processor import Processor

from music.backend.backend_services import AlbumService, SongService

lgr = logging.getLogger(__name__)


class PrimaryAPI(object):
	"""
	This class handles all the API endpoints visible to the user
	"""
	@csrf_exempt
	@enable_spa
	def accounts(self, request):
		"""
		This method lists all the accounts
		@param request: Request made by the user
		@return: Accounts
		@type: List
		"""
		try:
			accounts = list(AccountService().filter(~Q(state__name = 'Deleted')).values(
				'first_name', 'last_name', 'phone_number', 'email', 'gender', 'location', 'date_of_birth',
				'state__name', 'date_created').order_by('-date_created'))
			return JsonResponse({'status': 'success', 'data': accounts})
		except Exception as e:
			lgr.error('accounts exception: %s', e)
		return JsonResponse({'status': 'failed', 'message': 'Internal server error'})

	@csrf_exempt
	@enable_spa
	def albums(self, request):
		"""
		This method lists all the albums
		@param request: Request made by the user
		@return: Albums
		@type: dict
		"""
		try:
			albums = list(AlbumService().filter_album(~Q(state__name = 'Deleted')).order_by(
				'-date_created').values('key', 'album_title', 'artist', 'genre', 'state__name', 'date_created'))
			return JsonResponse({'status': 'success', 'data': albums})
		except Exception as e:
			lgr.error('albums exception: %s', e)
		return JsonResponse({'status': 'failed', 'message': 'Internal server error'})

	@csrf_exempt
	@enable_spa
	def songs(self, request):
		"""
		This method lists all the songs
		@param request: Request made by the user
		@return: Songs
		@type: List
		"""
		try:
			songs = list(SongService().filter_song(~Q(state__name = 'Deleted')).order_by('-date_created').values(
				'song_title', 'album__album_title', 'is_favorite', 'state__name', 'date_created'))
			return JsonResponse({'status': 'success', 'data': songs})
		except Exception as e:
			lgr.error('songs_endpoint Exception: %s', e)
		return JsonResponse({'status': 'failed', 'message': 'Internal server error'})

	@csrf_exempt
	@enable_spa
	def register_account(self, request):
		"""
		This api endpoint provides registration functionality to the user
		@param request: Http request made over the browser
		@return: http response
		"""
		try:
			data = {
				'first_name': request.POST.get('first_name'),
				'last_name': request.POST.get('last_name'),
				'phone_number': request.POST.get('phone_number'),
				'email': request.POST.get('email'),
				'date_of_birth': request.POST.get('date_of_birth'),
				'gender': request.POST.get('gender'),
				'pin': request.POST.get('pin'),
				'location': request.POST.get('location')
				}
			account = Processor().register_account(data)
			if account.get('status') == 'success':
				return JsonResponse({'status': 'success', 'message': 'Account registered successfully'})
			return JsonResponse({'status': 'failed', 'message': 'Bad request, try again'})
		except Exception as e:
			lgr.error('register_account endpoint Exception: %s', e)
		return JsonResponse({'status': 'failed', 'message': 'Internal server error'})

	@csrf_exempt
	def create_album(self, request):
		"""
		This method creates a new Album object into the db
		@return: Album
		"""
		try:
			data = {
				"state": request.POST.get('state'),
				"album_title": request.POST.get('album_title'),
				"artist": request.POST.get('artist'),
				"genre": request.POST.get('genre'),
				"album_logo": request.POST.get('album_logo')
				}
			album = Processor().create_album(data)
			if album['status'] == 'success':
				return JsonResponse({'status': 'success', 'message': 'Album created successfully.'})
			return JsonResponse({'status': 'failed', 'message': 'Bad request, try again'})
		except Exception as e:
			lgr.error('create_album api Exception: %s', e)
		return JsonResponse({'status': 'failed', 'message': 'Internal server error'})

	@csrf_exempt
	def create_song(self, request):
		"""
		This endpoint handles the create_song functionality
		@return: Song
		"""
		try:
			data = {
				'album_key': request.POST.get('album_key'),
				'song_title': request.POST.get('song_title'),
				}
			song = Processor().create_song(data)
			if song['status'] == 'success':
				return JsonResponse({'status': 'success', 'message': 'Song created successfully.'})
			return JsonResponse({'status': 'failed', 'message': 'Bad request, try again'})
		except Exception as e:
			lgr.error('create_song api Exception: %s', e)
		return JsonResponse({'status': 'failed', 'message': 'Internal server error'})
