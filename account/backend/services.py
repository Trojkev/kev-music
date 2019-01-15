import logging

from account.models import State, Account

lgr = logging.getLogger(__name__)


class StateService(object):
	"""
	This class handles all the CRUD operations relating to the State model i.e:
		1. get(*args, **kwargs)
		2. filter(*args, **kwargs)
		3. create(**kwargs)
		4. update(key, **kwargs)
	"""
	@staticmethod
	def get(*args, **kwargs):
		try:
			return State.objects.get(*args, **kwargs)
		except Exception as e:
			lgr.error('StateService().get Exception: %s', e)
			return None
	
	@staticmethod
	def filter(*args, **kwargs):
		try:
			return State.objects.filter(*args, **kwargs)
		except Exception as e:
			lgr.error('StateService().filter Exception: %s', e)
			return None
	
	@staticmethod
	def create(**kwargs):
		try:
			return State.objects.create(**kwargs)
		except Exception as e:
			lgr.error('StateService().create Exception: %s', e)
			return None
	
	@staticmethod
	def update(key, **kwargs):
		try:
			record = StateService().get(key = key)
			for attr, value in kwargs.items():
				setattr(record, attr, value)
			record.save()
			record.refresh_from_db()
			return record
		except Exception as e:
			lgr.error('StateService().update Exception: %s', e)
			return None


class AccountService(object):
	"""
	This class handles all the CRUD operations relating to the Account model i.e:
		1. get(*args, **kwargs)
		2. filter(*args, **kwargs)
		3. create(**kwargs)
		4. update(key, **kwargs)
	"""
	@staticmethod
	def get(*args, **kwargs):
		try:
			return Account.objects.get(*args, **kwargs)
		except Exception as e:
			lgr.error('AccountService().get Exception: %s', e)
			return None
	
	@staticmethod
	def filter(*args, **kwargs):
		try:
			return Account.objects.filter(*args, **kwargs)
		except Exception as e:
			lgr.error('AccountService().filter Exception: %s', e)
			return None
	
	@staticmethod
	def create(**kwargs):
		"""
		This method creates an Account with the provided parameters
		:@param kwargs: parameters passed for creating the account
		@return: Account | None
		"""
		try:
			return Account.objects.create(**kwargs)
		except Exception as e:
			lgr.error('AccountService().create Exception: %s', e)
			return None
	
	@staticmethod
	def update(key, **kwargs):
		try:
			record = AccountService().get(key = key)
			for attr, value in kwargs.items():
				setattr(record, attr, value)
			record.save()
			record.refresh_from_db()
			return record
		except Exception as e:
			lgr.error('AccountService().update Exception: %s', e)
			return None
