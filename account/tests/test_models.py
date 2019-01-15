import pytest
from mixer.backend.django import mixer

from account.models import State, Account

pytestmark = pytest.mark.django_db


class TestAccountModels(object):
	"""
	This class tests the Account app models
	"""
	def test_state(self):
		"""
		This method tests the State model
		@return: State | None
		"""
		obj = mixer.blend('account.State', name = 'Active')
		result = State.objects.get(pk = obj.id)
		assert result is not None, 'Should return a State object'
		
	def test_account(self):
		"""
		This method tests the Account model
		@return: Account | None
		"""
		state = mixer.blend('account.State', name = 'Active')
		obj = mixer.blend('account.Account', state = state)
		result = Account.objects.get(pk = obj.id)
		assert result is not None, 'Should return an Account object'
