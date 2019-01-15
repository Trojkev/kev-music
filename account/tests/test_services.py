import pytest
from mixer.backend.django import mixer

from account.backend.services import StateService, AccountService

pytestmark = pytest.mark.django_db


class TestStateService(object):
	"""
	This class tests all the CRUD operations of the State service
	"""
	def test_get(self):
		obj = mixer.blend('account.State', name = 'Active')
		result = StateService().get(pk = obj.id)
		assert result is not None, 'Should return a State object'
		
		result = StateService().get(pk = 2)
		assert result is None, 'Should return None'
		
	def test_filter(self):
		obj = mixer.cycle(2).blend('account.State', name = 'Active')
		result = StateService().filter(name = 'Active')
		assert len(result) == len(obj), 'Should return two State objects with name Active'
		
		result = StateService().filter(abc = 'Active')
		assert result is None, 'Should return None'
		
	def test_create(self):
		data = {
			'name': 'Favourite',
			'description': 'Favourite state'
			}
		result = StateService().create(**data)
		assert result is not None, 'Should create a State object'
		
		data = {
			'abc': '',
			'description': 'Favourite state'
			}
		result = StateService().create(**data)
		assert result is None, 'Should return None'
		
	def test_update(self):
		obj = mixer.blend('account.State', name = 'Active')
		result = StateService().update(obj.key, name = 'Inactive')
		assert result is not None, 'Should update State with a new name'
		
		result = StateService().update('abc', name = 'Inactive')
		assert result is None, 'Should return None'
		

class TestAccountService(object):
	"""
	This class tests all the CRUD operations of the Account service
	"""
	def test_get(self):
		state = mixer.blend('account.State', name = 'Active')
		obj = mixer.blend('account.Account', state = state)
		result = AccountService().get(pk = obj.id)
		assert result is not None, 'Should return an Account object'
		
		result = AccountService().get(pk = 2)
		assert result is None, 'Should return None'
		
	def test_filter(self):
		state = mixer.blend('account.State', name = 'Active')
		obj = mixer.cycle(2).blend('account.Account', first_name = 'Kev', state = state)
		result = AccountService().filter(state = state)
		assert len(result) == len(obj), 'Should return two Account objects with State active'
		
		result = AccountService().filter(abc = 'def')
		assert result is None, 'Should return None'
		
	def test_create(self):
		"""
		This method tests the create_account service
		@return: Account | None
		"""
		state = mixer.blend('account.State', name = 'Active')
		user = mixer.blend('auth.User')
		data = {
			'state': state,
			'user': user,
			'first_name': 'Kevin',
			'last_name': 'Macharia',
			'phone_number': '254717072416',
			'email': 'kelvinmacharia078@gmail.com',
			'location': 'Nairobi',
			'date_of_birth': '2000-01-01'
			}
		account = AccountService().create(**data)
		assert account is not None, 'Should create an account object'
		
		data = {
			'abc': state,
			'first_name': 123,
			'last_name': None,
			'phone_number': '254717072416',
			'email': 'kelvinmacharia078@gmail.com',
			'location': 'Nairobi'
			}
		account = AccountService().create(**data)
		assert account is None, 'Should return None'
		
	def test_update(self):
		state = mixer.blend('account.State', name = 'Active')
		account = mixer.blend('account.Account', state = state)
		result = AccountService().update(account.key, phone_number = '254717072416')
		assert result is not None, 'Should update account with a new phone_number'
		
		result = AccountService().update('abc', phone_number = '254717072416')
		assert result is None, 'Should return None'
