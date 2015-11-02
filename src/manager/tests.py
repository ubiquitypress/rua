from django.test import TestCase
from onetasker import models
from django.utils import timezone
import time
import datetime
from django.test import SimpleTestCase
from django.db.models import Q
from onetasker import views
from core import models as core_models
from core import logic as core_logic, task
import json
from django.http import HttpRequest
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import resolve, reverse
from  __builtin__ import any as string_any
import calendar
# Create your tests here.

class CoreTests(TestCase):

	# Dummy DBs
	fixtures = [
		'settinggroups',
		'settings',
		'langs',
		'cc-licenses',
		'role',
		'test_auth_data',
		'test_review_data',
		'test_core_data',
		'test_index_assignment_data',
		'test_copyedit_assignment_data',

	]
  # Helper Function
	def getmessage(cls, response):
		"""Helper method to return first message from response """
		for c in response.context:
			message = [m for m in c.get('messages')][0]
			if message:
				return message

	def setUp(self):
		self.client = Client(HTTP_HOST="testing")
		self.user = User.objects.get(username="rua_user")
		self.user.save()
		self.book = core_models.Book.objects.get(pk=1)


		login = self.client.login(username="rua_user", password="root")
		self.assertEqual(login, True)

	def tearDown(self):
		pass

	def test_set_up(self):
		"""
		testing set up
		"""
		self.assertEqual(self.user.username=="rua_user", True)
		self.assertEqual(self.user.email=="fake_user@fakeaddress.com", True)
		self.assertEqual(self.user.first_name=="rua_user_first_name", True)
		self.assertEqual(self.user.last_name=="rua_user_last_name", True)
		self.assertEqual(self.user.profile.institution=="rua_testing", True)
		self.assertEqual(self.user.profile.country=="GB", True)

	def test_manager_access_staff(self):
		resp = self.client.get(reverse('manager_index'))
		content =resp.content
		
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)

	def test_manager_access_not_staff(self):
		login = self.client.login(username="rua_reviewer", password="tester")
		resp = self.client.get(reverse('manager_index'))
		
		self.assertEqual(resp.status_code, 302)
		self.assertEqual(resp['Location'], "http://testing/admin/login/?next=/manager/")
	
	def test_clear_cache(self):
		resp = self.client.get(reverse('manager_flush_cache'))
		self.assertEqual(resp.status_code, 302)
		self.assertEqual(resp['Location'], "http://testing/manager/")
		resp = self.client.get(reverse('manager_index'))
		message = self.getmessage(resp)
		self.assertEqual(message.message, "Memcached has been flushed.")


