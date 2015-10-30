from django.test import TestCase
from author import models
from core import models as core_models
from django.utils import timezone
import time
import datetime
from django.test import SimpleTestCase
from django.db.models import Q
from author import views
import json
from django.http import HttpRequest
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import resolve, reverse
from  __builtin__ import any as string_any
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
		'test_core_data',
		'test_review_data',
	]

	def setUp(self):
		self.client = Client(HTTP_HOST="testing")
		self.user = User.objects.get(username="rua_author")
		self.user.save()
		self.book = core_models.Book.objects.get(pk=1)

		login = self.client.login(username=self.user.username, password="tester")
		self.assertEqual(login, True)

	def tearDown(self):
		pass
	
	def test_dashboard(self):
		resp =  self.client.get(reverse('author_dashboard'))
		content =resp.content
		
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)
	def test_submission(self):
		resp =  self.client.get(reverse('author_submission',kwargs={'submission_id':self.book.id}))
		content =resp.content
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)
		self.assertEqual("AUTHORS" in content, True)
		authors = self.book.author.all()
		for author in authors:
			self.assertEqual( author.full_name() in content, True)
		self.assertEqual("DESCRIPTION" in content, True)
		self.assertEqual( self.book.description in content, True)
		self.assertEqual("COVER LETTER" in content, True)
		self.assertEqual( self.book.cover_letter in content, True)
		self.assertEqual("REVIEWER SUGGESTIONS" in content, True)
		self.assertEqual( self.book.reviewer_suggestions in content, True)
		self.assertEqual("COMPETING INTERESTS" in content, True)
		self.assertEqual( self.book.competing_interests in content, True)
	
	def test_submission_status(self):
		resp =  self.client.get(reverse('status',kwargs={'submission_id':self.book.id}))
		content =resp.content
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)
		self.assertEqual("Current Status" in content, True)
		self.assertEqual( "Submission Progress" in content, True)
		self.assertEqual( "Review" in content, True)
		self.assertEqual( "Submission" in content, True)
	
	def test_submission_tasks(self):
		resp =  self.client.get(reverse('tasks',kwargs={'submission_id':self.book.id}))
		content =resp.content
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)
		self.assertEqual("My Tasks" in content, True)
		self.assertEqual("No outstanding tasks" in content, True)
		self.typeset_assignment= core_models.TypesetAssignment.objects.get(pk=1)
		self.typeset_assignment.author_invited=timezone.now()
		self.typeset_assignment.save()
		resp =  self.client.get(reverse('tasks',kwargs={'submission_id':self.book.id}))
		content =resp.content
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)
		self.assertEqual("My Tasks" in content, True)
		self.assertEqual("No outstanding tasks" in content, False)
		self.assertEqual("Typesetting Review" in content, True)
		resp =  self.client.get(reverse('author_dashboard'))
		content =resp.content
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)
		self.assertEqual("Typesetting Review" in content, True)
		self.assertEqual("Invited on" in content, True)

	def test_author_review_review_round(self):
		resp =  self.client.get(reverse('review',kwargs={'submission_id':self.book.id}))
		content =resp.content
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)
		self.assertEqual("btn-success" in content, False)
		self.review_round=core_models.ReviewRound(book=self.book,round_number=1)
		self.review_round.save()
		resp =  self.client.get(reverse('review',kwargs={'submission_id':self.book.id}))
		content =resp.content
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)
		self.assertEqual("btn-success" in content, True)
		resp =  self.client.get(reverse('view_review_round',kwargs={'round_id':1,'submission_id':self.book.id}))
		content =resp.content
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)
		self.assertEqual("btn-success" in content, True)
		self.assertEqual("ROUND 1" in content, True)
	def test_author_editing(self):
		self.book.stage.current_stage='editing'
		self.book.stage.editing=timezone.now()
		self.book.stage.save()
		self.book.save()
		resp =  self.client.get(reverse('editing',kwargs={'submission_id':self.book.id}))
		content =resp.content
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)
		self.assertEqual("COPYEDITING" in content, True)
		self.assertEqual("INDEXING" in content, True)
		self.assertEqual("Stage has not been initialised." in content, True)
		self.book.stage.copyediting=timezone.now()
		self.book.stage.indexing=timezone.now()
		self.book.stage.save()
		self.book.save()
		resp =  self.client.get(reverse('editing',kwargs={'submission_id':self.book.id}))
		content =resp.content
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)
		self.assertEqual("COPYEDITING" in content, True)
		self.assertEqual("INDEXING" in content, True)
		self.assertEqual("Stage has not been initialised." in content, False)

	def test_author_production(self):
		self.book.stage.current_stage='production'
		self.book.stage.production=timezone.now()
		self.book.stage.save()
		self.book.save()
		resp =  self.client.get(reverse('author_production',kwargs={'submission_id':self.book.id}))
		content =resp.content
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)
		self.assertEqual("Typesetting" in content, True)
		self.assertEqual("Stage has not been initialised." in content, True)
		self.book.stage.typesetting=timezone.now()
		self.book.stage.save()
		self.book.save()
		resp =  self.client.get(reverse('author_production',kwargs={'submission_id':self.book.id}))
		content =resp.content
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)
		self.assertEqual("Typesetting" in content, True)
		self.assertEqual("Stage has not been initialised." in content, False)




