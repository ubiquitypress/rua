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
from django.core import management
from revisions import models as revision_models
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
		resp = self.client.post(reverse('editor_dashboard'), {'filter': 'review', 'order': 'title','search':'rua'})
		content = resp.content
		self.assertTrue(resp.status_code, 200)
		self.assertEqual("Book %s: %s %s %s" % (self.book.id,self.book.prefix,self.book.title,self.book.subtitle) in content,False)
	def test_submission(self):
		self.book.stage.current_stage='submission'
		self.book.stage.review=None
		self.book.stage.save()
		self.book.save()
		book = core_models.Book.objects.get(pk=1)
		self.assertEqual(book.stage.current_stage=='submission',True)
		resp =  self.client.get(reverse('editor_submission',kwargs={'submission_id':self.book.id}))
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
		resp =  self.client.post(reverse('editor_submission',kwargs={'submission_id':self.book.id}),{'review':''})
		book = core_models.Book.objects.get(pk=1)
		self.assertEqual(book.stage.current_stage=='review',True)
	
	def test_submission_status(self):
		resp =  self.client.get(reverse('editor_status',kwargs={'submission_id':self.book.id}))
		content =resp.content
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)
		self.assertEqual("Current Status" in content, True)
		self.assertEqual( "Submission Progress" in content, True)
		self.assertEqual( "Review" in content, True)
		self.assertEqual( "Submission" in content, True)
	
	def test_submission_tasks(self):
		resp =  self.client.get(reverse('editor_tasks',kwargs={'submission_id':self.book.id}))
		content =resp.content
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)
		self.assertEqual("My Tasks" in content, True)
		self.assertEqual("No outstanding tasks" in content, True)
		self.typeset_assignment= core_models.TypesetAssignment.objects.get(pk=1)
		self.typeset_assignment.accepted=timezone.now()
		self.typeset_assignment.requestor=self.user
		self.typeset_assignment.author_invited=timezone.now()
		self.typeset_assignment.author_completed=timezone.now()
		self.typeset_assignment.save()
		resp =  self.client.get(reverse('editor_tasks',kwargs={'submission_id':self.book.id}))
		content =resp.content
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)
		self.assertEqual("My Tasks" in content, True)
		self.assertEqual("No outstanding tasks" in content, False)
		self.assertEqual("Typesetting Review" in content, True)

	def test_editor_review_review_round(self):
		book = core_models.Book.objects.get(pk=1)
		self.assertEqual(book.stage.current_stage=='review',True)
		resp =  self.client.get(reverse('editor_review',kwargs={'submission_id':self.book.id}))
		content =resp.content
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)
		self.assertEqual("btn-task" in content, False)
		resp =  self.client.post(reverse('editor_review',kwargs={'submission_id':self.book.id}),{'new_round':''})
		resp =  self.client.get(reverse('editor_review',kwargs={'submission_id':self.book.id}))
		content =resp.content
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)
		self.assertEqual("btn-task" in content, True)
		resp =  self.client.get(reverse('editor_review_round',kwargs={'round_number':1,'submission_id':self.book.id}))
		content =resp.content
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)
		self.assertEqual("btn-task" in content, True)
		self.assertEqual("ROUND 1" in content, True)
		
	def test_editor_editing(self):
		resp =  self.client.post(reverse('editor_review',kwargs={'submission_id':self.book.id}),{'move_to_editing':''})
		book = core_models.Book.objects.get(pk=1)
		self.assertEqual(book.stage.current_stage=='editing',True)

		resp =  self.client.get(reverse('editor_editing',kwargs={'submission_id':self.book.id}))
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
		resp =  self.client.get(reverse('editor_editing',kwargs={'submission_id':self.book.id}))
		content =resp.content
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)
		self.assertEqual("COPYEDITING" in content, True)
		self.assertEqual("INDEXING" in content, True)
		self.assertEqual("Stage has not been initialised." in content, False)


		management.call_command('loaddata', 'test_copyedit_assignment_data.json', verbosity=0)
		management.call_command('loaddata', 'test_index_assignment_data.json', verbosity=0)
		onetasker= User.objects.get(username="rua_onetasker")
		resp =  self.client.get(reverse('view_copyedit',kwargs={'copyedit_id':1,'submission_id':self.book.id}))
		content =resp.content
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)
		self.assertEqual("COPYEDITING" in content, True)
		self.assertEqual("INDEXING" in content, True)
		self.assertEqual("Stage has not been initialised." in content, False)
		title = "COPYEDITING: %s %s" % (onetasker.first_name.upper(), onetasker.last_name.upper()) 
		self.assertEqual(title in content, True)
		resp =  self.client.get(reverse('view_index',kwargs={'index_id':1,'submission_id':self.book.id}))
		content =resp.content
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)
		self.assertEqual("COPYEDITING" in content, True)
		self.assertEqual("INDEXING" in content, True)
		self.assertEqual("Stage has not been initialised." in content, False)
		title = "INDEXING: %s %s" % (onetasker.first_name.upper(), onetasker.last_name.upper()) 
		self.assertEqual(title in content, True)

	def test_editor_production(self):
		self.book.stage.current_stage='production'
		self.book.stage.production=timezone.now()
		self.book.stage.save()
		self.book.save()
		resp =  self.client.get(reverse('editor_production',kwargs={'submission_id':self.book.id}))
		content =resp.content
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)
		self.assertEqual("Typesetting" in content, True)
		self.assertEqual("Stage has not been initialised." in content, True)
		self.book.stage.typesetting=timezone.now()
		self.book.stage.save()
		self.book.save()
		resp =  self.client.get(reverse('editor_production',kwargs={'submission_id':self.book.id}))
		content =resp.content
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)
		self.assertEqual("Typesetting" in content, True)
		self.assertEqual("Stage has not been initialised." in content, False)
		
		resp =  self.client.get(reverse('view_typesetter',kwargs={'typeset_id':1,'submission_id':self.book.id}))
		content =resp.content
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)
		self.assertEqual("Typesetting" in content, True)
		self.assertEqual("Stage has not been initialised." in content, False)
		onetasker= User.objects.get(username="rua_onetasker")
		title = "TYPESETTING: %s %s" % (onetasker.first_name.upper(), onetasker.last_name.upper()) 
		self.assertEqual(title in content, True)
	
	def test_editor_publish(self):
		resp =  self.client.post(reverse('editor_review',kwargs={'submission_id':self.book.id}),{'move_to_editing':''})
		self.book.stage.current_stage='production'
		self.book.stage.production=timezone.now()
		self.book.stage.save()
		self.book.save()
		resp =  self.client.post(reverse('editor_publish',kwargs={'submission_id':self.book.id}))
		self.assertEqual(resp.status_code, 302)
		self.assertEqual(resp['Location'], "http://testing/editor/submission/1/")

		book = core_models.Book.objects.get(pk=1)
		self.assertEqual(book.stage.current_stage=='published',True)

	def test_request_revisions(self):
		resp =  self.client.get(reverse('request_revisions',kwargs={'submission_id':self.book.id,'returner':'review'}))
		content =resp.content
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)
		resp =  self.client.post(reverse('request_revisions',kwargs={'submission_id':self.book.id,'returner':'review'}),{'notes_from_editor':'notes','due':'2015-11-30','id_email_text':'Hi User'})
		self.assertEqual(resp.status_code, 302)
		self.assertEqual(resp['Location'], "http://testing/editor/submission/1/review/")
		self.client.login(username="rua_author", password="tester")
		revision = revision_models.Revision.objects.get(book=self.book)
		resp =  self.client.post(reverse('author_revision',kwargs={'submission_id':self.book.id,'revision_id':revision.id}),{'cover_letter':'updated cover letter'})
		self.client.login(username="rua_editor", password="tester")
		resp = self.client.get(reverse('editor_dashboard'))
		content = resp.content
		self.assertTrue(resp.status_code, 200)
		self.assertEqual("403" in content, False)
		notification = "Revisions submitted for %s" % self.book.title
		self.assertEqual(notification in content, True)



