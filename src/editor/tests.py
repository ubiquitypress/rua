from django.test import TestCase
from django.core.urlresolvers import resolve, reverse
from django.test.client import Client
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
import time
import datetime
from django.test import SimpleTestCase
from django.db.models import Q
from editor import views,models
from core import models as core_models
from review import models as review_models
from submission import models as submission_models
from core import logic as core_logic, task
import json
from django.http import HttpRequest
from  __builtin__ import any as string_any
import calendar

class EditorTests(TestCase):

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
		'test_manager_data',
		'test_submission_checklist_item_data',
		'test_proposal_form',
	]

	# Helper Function
	def getmessage(cls, response):
		"""Helper method to return first message from response """
		for c in response.context:
			message = [m for m in c.get('messages')][0]
			if message:
				return message

	def setUp(self):
		self.client = Client()
		self.user = User.objects.get(username="rua_editor")
		self.book = core_models.Book.objects.get(pk=1)
		login = self.client.login(username='rua_editor', password='tester')
		self.assertEqual(login, True)

	def tearDown(self):
		pass

	def test_editor_dashboard(self):
		"""Fetches the editor dashboard"""
		resp = self.client.get(reverse('editor_dashboard'))
		content = resp.content
		self.assertTrue(resp.status_code, 200)
		self.assertEqual("403" in content, False)
		self.assertContains(resp, "Book %s: %s %s %s" % (self.book.id,self.book.prefix,self.book.title,self.book.subtitle))

	def test_editor_dashboard_filter(self):
		"""Tests out the filters on the Editor Dashboard"""
		self.book.stage.current_stage='submission'
		self.book.stage.review=None
		self.book.stage.save()
		self.book.save()
		resp = self.client.post(reverse('editor_dashboard'), {'filter': 'review', 'order': 'title'})
		content = resp.content
		self.assertTrue(resp.status_code, 200)
		self.assertEqual("Book %s: %s %s %s" % (self.book.id,self.book.prefix,self.book.title,self.book.subtitle) in content,False)


