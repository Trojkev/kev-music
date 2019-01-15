import logging
import re
import datetime
from dateutil.parser import parse

lgr = logging.getLogger(__name__)


class Validator:
	"""
	Handles validator methods for common user inputs
	"""
	def __init__(self):
		pass

	@staticmethod
	def validate_name(name, single=False, alphabet=True, min_length=3, max_length=100):
		"""
		Return True if the length of name is within the range of min_length & max_length,
		false otherwise.
		:param name: name passed to be validated
		:param single: Should be true if a single word is allowed. False otherwise.
		:param alphabet: Uses regex: characters from a-z, A-Z can contain ' or "
		:param min_length: minimum length of name
		:param max_length: maximum length of name
		:return: True if valid or False if Invalid
		"""
		try:
			name = str(name).strip()

			if alphabet:
				if not re.match(r"(^[a-zA-Z\s\'\"]+$)", name):
					return False

			if single and len(name.split()) > 1:
				return False

			if min_length <= len(name) <= max_length:
				return True
		except Exception as e:
			lgr.error('validate_name: %s', e)
		return False

	@staticmethod
	def validate_email(email):
		"""
		Checks if the email provided is a valid email address
		Should be of characters more than 7
		:param email:
		:return: True if valid, false otherwise
		"""
		try:
			if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
				return True

		except Exception as e:
			lgr.error('validate_email: %s', e)
		return False

	@staticmethod
	def validate_phone_number(phone_number):
		"""
		Checks the validity of a kenyan phone number

		:param phone_number:
		:return: True if valid, False otherwise
		"""
		try:
			if re.match(r"(^(?:254|\+254|0)?(7(\d){8}))", phone_number):
				return True
		except Exception as e:
			lgr.error('validate_phone_number: %s', e)
		return False

	@staticmethod
	def validate_id_number(id_number):
		"""
		Checks if the id_number is valid by checking the length and type.
		:param id_number: Id_number from payload
		:return: True if valid, False otherwise
		"""
		try:
			if 7 <= len(id_number) <= 8 and id_number.isdigit():
				return True
		except Exception as e:
			lgr.error('validate_id_number: %s', e)
		return False

	@staticmethod
	def validate_date(date):
		"""
		Validates the date using the DD/MM/YY format
		:param date: Date provided by payload
		:return: True if valid, False otherwise
		"""
		try:
			if isinstance(date, str):
				date = parse(date)
			if isinstance(date, (datetime.date, datetime.datetime)):
				return True
		except Exception as e:
			lgr.error('validate_date: %s', e)
		return False

	@staticmethod
	def validate_pin(pin):
		"""
		Checks if a pin is valid by checking the length and type
		:param pin: Provided by payload
		:return: True if valid, False otherwise
		"""
		try:
			if len(pin) == 4 and pin.isdigit():
				return True
		except Exception as e:
			lgr.error('validate_pin: %s', e)
		return False
