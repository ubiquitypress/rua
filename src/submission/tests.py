from django.test import TestCase
from submission import models
from django.utils import timezone
import time
import datetime
from django.test import SimpleTestCase
from django.db.models import Q
from manager import views
from core import models as core_models
from review import models as review_models
from submission import models as submission_models
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

	def test_submission_proposal(self):
		resp = self.client.get(reverse('proposal_start'))
		content =resp.content
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)

		proposal_form_id = core_models.Setting.objects.get(name='proposal_form').value
		proposal_form = core_models.ProposalForm.objects.get(pk=proposal_form_id)
		fields=core_models.ProposalFormElementsRelationship.objects.filter(form=proposal_form)
		self.assertEqual('name="title"' in content, True)
		self.assertEqual('name="subtitle"' in content, True)
		self.assertEqual('name="author"' in content, True)

		for field in fields:
			self.assertEqual('name="%s"' % field.element.name in content, True)
		forms = models.Proposal.objects.all()
		self.assertEqual(len(forms), 0)
		resp=self.client.post(reverse('proposal_start'),{"title":"rua_proposal_title","subtitle":"rua_proposal_subtitle","author":"rua_user","rua_element":"example","rua_element_2":"example"})
		forms = models.Proposal.objects.all()
		self.assertEqual(len(forms), 1)


		
		
		
