from django.conf.urls import url

from api.views import PrimaryAPI

urlpatterns = [
	url(r'^accounts/$', PrimaryAPI().accounts, name = 'accounts'),
	url(r'^albums/$', PrimaryAPI().albums, name = 'albums'),
	url(r'^songs/$', PrimaryAPI().songs, name = 'songs'),
	url(r'^register_account/$', PrimaryAPI().register_account, name = 'register_account'),
	url(r'^create_album/$', PrimaryAPI().create_album, name = 'create_album'),
	url(r'^create_song/$', PrimaryAPI().create_song, name = 'create_song'),
	]
