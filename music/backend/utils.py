import base64
import logging
import hashlib

from datetime import date, datetime

from decimal import Decimal

import binascii

import os
from django.db.models import Q

lgr = logging.getLogger(__name__)


class HashText:
	"""
	Handles hash_text method
	"""

	def __init__(self):
		pass

	@staticmethod
	def hash_text(text):
		hashed_str = None
		try:
			plain_text = str(text)
			m = hashlib.sha1()
			m.update(plain_text)
			x = m.hexdigest()
			n = hashlib.sha512()
			n.update(x)
			hashed_str = n.hexdigest()
		except Exception as e:
			lgr.error('hash_pin error:%s' % e)
			return hashed_str
		return hashed_str


class CleanPhoneNumber:
	"""
	Defines clean_phone_number method
	"""

	def __init__(self):
		pass

	@staticmethod
	def clean_phone_number(phone):
		try:
			if phone[:1] == "0":
				phone = "254%s" % phone[1:10]
			elif phone[:1] == "7":
				phone = "254%s" % phone[0:9]
			elif phone[:1] == "+":
				phone = phone[1:13]
		except Exception as e:
			lgr.error("%s" % e)
		return phone


def json_super_serializer(obj):
	"""
	Automatic serializer for objects not serializable by default by the JSON serializer.
	Includes datetime, date, Decimal
	@return: Serialized object to be returned or raises an exception.
	"""
	if isinstance(obj, (datetime, date)):
		return obj.isoformat()
	if isinstance(obj, Decimal):
		return str(round(Decimal(obj), 2))
	raise TypeError("Type %s not serializable" % type(obj))


def build_search_query(fields, value):
	"""
	Builds the search queries from the fields.
	Uses __contains with the fields
	:param fields: A list or tuple of field names.
	:type fields: list | tuple
	:param value: The value to search for in the records.
	:type value: str
	:return: Django Q queries ORed together.
	:@rtype: Q | None
	"""
	try:
		fields = list(fields)
		if len(fields) > 0:
			query = Q(('%s__contains' % str(fields.pop(len(fields) - 1)), str(value)))
			for fl in fields:
				if fl != '' and str(value) != '':
					query |= Q(('%s__contains' % fl, str(value)))
			return query
	except Exception as e:
		lgr.exception('build_search_query Exception: %s', e)
	return ~Q(date_created = None)


def process_dt_ordering(order, columns = list(), default_sort = '-date_created'):
	""" Usage: *process_dt_ordering(order, columns)
	Gets the ordering sent from a DT request and parses it accordingly.
	@param order: The DT request order field. i.e. [{column:0, dir: 'asc'}]
	@param columns: The columns as ordered on the client-side.
	@param default_sort: The default sorting criteria if an exception occurs. String.
	@return: A tuple containing the appropriate columns.
	@rtype: tuple
	"""
	try:
		ordering = list()
		order = list(order)
		if len(order) > 0:
			for ord_item in order:
				ord_item = dict(ord_item)
				column = int(ord_item.get('column', 0))
				sort = str(ord_item.get('dir', 'asc'))
				if sort == 'asc':
					sort = ''
				else:
					sort = '-'
				if len(columns) > column:
					if len(str(columns[column])) > 3:
						ordering.append(str(sort + str(columns[column])))
				elif len(str(ord_item.get('column', 0))) > 3:
					ordering.append(str(sort + str(ord_item.get('column', ''))))
		if len(ordering) > 0:
			return tuple(ordering)
		return default_sort,
	except Exception as e:
		lgr.exception('process_dt_ordering Exception: %s', e)
	return default_sort,


def generate_token():
	"""
	Generates a standard token to be used for ABCD + etc.
	@return:
	"""
	try:
		return base64.b64encode(binascii.hexlify(os.urandom(15)).decode())
	except Exception as e:
		lgr.exception('generate_token Exception: %s', e)
	return None


def generate_pin(length = 4):
	"""
	Generates a string of digits of the provided length defaulting to 4
	@return: a string of randomly generated digits 
	"""
	try:
		from random import randint
		return ''.join(str(x) for x in range(1000, 9999))
	except Exception as e:
		lgr.exception('generate_pin exception: %s', e)
	return None
