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

	def test_onetasker_access(self):
		resp = self.client.get(reverse('onetasker_dashboard'))
		content =resp.content
		
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)

	def test_not_onetasker_access(self):
		login = self.client.login(username="rua_reviewer", password="tester")
		resp = self.client.get(reverse('onetasker_dashboard'))
		content =resp.content
		
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, True)

	def test_onetasker_dashboard(self):
		response = self.client.get(reverse('user_dashboard'))
		self.assertRedirects(response, "http://testing/tasks/", status_code=302, target_status_code=200, host=None, msg_prefix='', fetch_redirect_response=True)
		onetasker_tasks = core_logic.onetasker_tasks(self.user)
		active_count=len(onetasker_tasks.get('active'))
		self.assertEqual(active_count, 3)
		response = self.client.get(reverse('onetasker_dashboard'))
		content =response.content
		self.assertEqual(response.status_code, 200)
		self.assertEqual("403" in content, False)
		self.assertEqual("Copyedit" in content, True)
		self.assertEqual("Indexing" in content, True)
		self.assertEqual("Typesetting" in content, True)
		self.assertEqual("rua_title" in content, True)

	def test_onetasker_view_task(self):
		onetasker_tasks = core_logic.onetasker_tasks(self.user)
		active_tasks = onetasker_tasks.get('active')
		for task in active_tasks:
			response = self.client.get(reverse('onetasker_task_hub',kwargs={'assignment_type':task.get('type'),'assignment_id':task.get('assignment').id}))
			content =response.content
			self.assertEqual(response.status_code, 200)
			self.assertEqual("403" in content, False)
			self.assertEqual("You can accept or reject this task" in content, True)
			self.assertEqual("I Accept" in content, True)
			self.assertEqual("I Decline" in content, True)

			assignment=task.get('assignment')
			assignment.accepted=timezone.now()
			assignment.save()
			self.assignment= core_models.ReviewAssignment.objects.get(pk=1)
			response = self.client.post(reverse('onetasker_task_hub',kwargs={'assignment_type':task.get('type'),'assignment_id':task.get('assignment').id}), {'accept': 'I Accept'})
			content =response.content
			self.assertEqual(response.status_code, 200)
			self.assertEqual("403" in content, False)
			month = time.strftime("%m")
			day = int(time.strftime("%d"))
			year = time.strftime("%Y")
			month_name = calendar.month_name[int(month)]
			month_name=month_name[:3]

			message = "You accepted on %s %s %s" % (day,month_name,year)
			self.assertEqual(message in content, True)




