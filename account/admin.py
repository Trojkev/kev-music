# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.
from account.models import State, Account, Artist


class StateAdmin(admin.ModelAdmin):
	list_display = ('name', 'description')
	search_fields = ('name', 'description')

admin.site.register(State, StateAdmin)


class AccountAdmin(admin.ModelAdmin):
	list_display = [
		'phone_number', 'first_name', 'last_name', 'location', 'gender', 'email',
		'state', 'date_of_birth', 'date_created']
	search_fields = [
		'phone_number', 'first_name', 'last_name', 'location',
		'date_of_birth', 'gender', 'email']

admin.site.register(Account, AccountAdmin)


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
	list_display = ('name', 'alias', 'state', 'date_modified', 'date_created')
	search_fields = ('name', 'alias', 'state__name')