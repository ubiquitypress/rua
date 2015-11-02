from django.test import TestCase
from onetasker import models
from django.utils import timezone
import time
import datetime
from django.test import SimpleTestCase
from django.db.models import Q
from onetasker import views
from core import models as core_models
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

	def setUp(self):
		self.client = Client(HTTP_HOST="testing")
		self.user = User.objects.get(username="rua_onetasker")
		self.user.save()
		self.book = core_models.Book.objects.get(pk=1)


		login = self.client.login(username="rua_onetasker", password="tester")
		self.assertEqual(login, True)

	def tearDown(self):
		pass

	def test_set_up(self):
		"""
		testing set up
		"""
		self.assertEqual(self.user.username=="rua_onetasker", True)
		self.assertEqual(self.user.email=="fake_onetasker@fakeaddress.com", True)
		self.assertEqual(self.user.first_name=="rua_onetasker_first_name", True)
		self.assertEqual(self.user.last_name=="rua_onetasker_last_name", True)
		self.assertEqual(self.user.profile.institution=="rua_testing", True)
		self.assertEqual(self.user.profile.country=="GB", True)