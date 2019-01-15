# -*- coding: utf-8 -*-
import uuid

from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class State(models.Model):
	name = models.CharField(max_length = 20)
	description = models.TextField(blank = True, null = True)
	key = models.CharField(max_length = 255, default = uuid.uuid4, editable = False)
	date_modified = models.DateTimeField(auto_now = True)
	date_created = models.DateTimeField(auto_now_add = True)
	
	def __unicode__(self):
		return '%s' % self.name


class Account(models.Model):
	user = models.OneToOneField(User)
	first_name = models.CharField(max_length = 30)
	last_name = models.CharField(max_length = 30, null = True, blank = True)
	phone_number = models.CharField(max_length = 15, unique = True)
	email = models.CharField(max_length = 50)
	date_of_birth = models.DateField()
	gender = models.CharField(max_length = 7)
	pin_hash = models.CharField(max_length = 255, default = '')
	location = models.CharField(max_length = 50, null = True, blank = True)
	state = models.ForeignKey(State)
	failed_login_attempts = models.IntegerField(blank = True, null = True, default = 0)
	key = models.CharField(max_length = 255, default = uuid.uuid4, editable = False)
	date_modified = models.DateTimeField(auto_now = True)
	date_created = models.DateTimeField(auto_now_add = True)
	
	def __unicode__(self):
		return '%s - %s' % (self.first_name, self.phone_number)
