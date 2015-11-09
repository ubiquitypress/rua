from django.test import TestCase
from core import models
from django.utils import timezone
import time
import datetime
from django.test import SimpleTestCase
from django.db.models import Q
from core import views
import json
from django.http import HttpRequest
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import resolve, reverse
from  __builtin__ import any as string_any
import tempfile
from django.test.utils import setup_test_environment

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
	# Helper Function
	def getmessage(cls, response):
		"""Helper method to return first message from response """
		for c in response.context:
			message = [m for m in c.get('messages')][0]
			if message:
				return message
	def get_specific_message(cls, response,number):
		"""Helper method to return first message from response """
		for c in response.context:
			message = [m for m in c.get('messages')][number]
			if message:
				return message
	def setUp(self):
		self.client = Client(HTTP_HOST="testing")
		self.user = User.objects.get(pk=1)
		self.user.save()
		setup_test_environment()
		login = self.client.login(username=self.user.username, password="root")
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

##############################################	Fixture Tests	 ##############################################		

	def test_roles_fixture(self):
		"""
		testing roles fixture
		"""
		roles = ["Reader","Author","Copyeditor","Reviewer","Press Editor","Book Editor","Series Editor","Indexer","Typesetter"]
		roles_exist=True	
		for role_name in roles:
			try:
				role = models.Role.objects.get(name=role_name)
			except models.Role.DoesNotExist:
				roles_exist = False
		number_of_roles = len(models.Role.objects.all())
		self.assertEqual(number_of_roles==9, True)
		self.assertEqual(roles_exist, True)
	
	def test_settings_fixture(self):
		"""
		testing settings fixture
		"""
		settings = ["accronym","base_url","ci_required","city","copyedit_author_instructions","copyedit_instructions","description","footer","index_instructions","press_name","proposal_form","review_suggestions","submission_checklist_help","submission_guidelines","typeset_author_instructions","typeset_instructions","accepted_reminder","author_copyedit_request","author_submission_ack","author_typeset_request","contract_author_sign_off","copyedit_request","editor_submission_ack","external_review_request","from_address","index_request","overdue_reminder","proposal_accept","proposal_decline","proposal_request_revisions","proposal_review_request","request_revisions","review_request","revisions_reminder_email","typeset_request","typesetter_typeset_request","unaccepted_reminder","brand_header","favicon","remind_accepted_reviews","remind_overdue_reviews","remind_unaccepted_reviews","revisions_reminder"]
		settings_exist=True	
		for setting_name in settings:
			try:
				setting = models.Setting.objects.get(name=setting_name)
			except models.Setting.DoesNotExist:
				settings_exist = False
		number_of_settings = len(models.Setting.objects.all())
		self.assertEqual(number_of_settings==43, True)
		self.assertEqual(settings_exist, True)
	
	def test_setting_groups_fixture(self):
		"""
		testing setting groups fixture
		"""
		setting_groups = ["general","page","email","look","cron"]
		setting_groups_exist=True
		for group in setting_groups:
			try:
				group = models.SettingGroup.objects.get(name=group)
			except models.SettingGroup.DoesNotExist:
				setting_groups_exist = False
		number_of_setting_groups = len(models.SettingGroup.objects.all())
		self.assertEqual(number_of_setting_groups==5, True)
		self.assertEqual(setting_groups_exist, True)

	def test_cc_licenses_fixture(self):
		"""
		testing cc licenses fixture
		"""
		license_codes = ["cc-4-by","cc-4-by-sa","cc-4-by-nd","cc-4-by-nc","cc-4-by-nc-nd","cc-4-by-nd-sa"]
		license_codes_exist=True
		for code in license_codes:
			try:
				group = models.License.objects.get(code=code)
			except models.License.DoesNotExist:
				license_codes_exist = False
		number_of_licenses = len(models.License.objects.all())
		self.assertEqual(number_of_licenses==6, True)
		self.assertEqual(license_codes_exist, True)

	def test_langs_fixture(self):
		"""
		testing langs fixture
		"""
		langs= ["abk","afr","afa","amh","anp","apa","ara","hye","asm","ast","aus","aze","ban","bat","bas","bak","eus","bel","ben","ber","bos","bre","bul","mya","cat","cel","cai","che","chr","zho","cor","cos","hrv","ces","dak","dan","dum","nld","eng","est","fao","fij","fil","fin","fiu","fra","gla","car","glg","lug","gay","gba","gez","kat","deu","gmh","goh","gem","gil","hat","haw","heb","hin","hun","isl","ind","gle","ita","jpn","tlh","kon","kor","kur","kru","lat","lav","lit","nds","lus","ltz","mkd","mlg","msa","mal","mlt","mni","mri","myn","moh","mol","mon","new","nep","non","nai","nor","nno","pag","pan","paa","fas","phi","pol","por","ron","rom","rus","smo","sco","srp","iii","scn","sla","slk","slv","sog","som","son","wen","spa","zgh","suk","sun","swa","swe","gsw","syr","tha","tog","ton","tsi","tso","tsn","tum","tur","ukr","urd","uzb","vai","ven","vie","cym","yap","yid","zap","zha","zul"]
		langs_exist=True
		for lang in langs:
			try:
				language = models.Language.objects.get(code=lang)
			except models.Language.DoesNotExist:
				langs_exist = False
		number_of_langs = len(models.Language.objects.all())
		self.assertEqual(number_of_langs==147, True)
		self.assertEqual(langs_exist, True)

##############################################	Model Tests	 ##############################################		

	def test_author_model(self):
		"""
		test author model
		"""
		self.author = models.Author.objects.get(pk=1)
		self.author.save()
		#model functions
		fullname="%s %s" % ("rua_author_first_name","rua_author_last_name")
		unicode_text=u'%s - %s %s' % (str(1), "rua_author_first_name", "rua_author_last_name")
		self.assertEqual(self.author.__repr__()==unicode_text,True)
		self.assertEqual(self.author.__unicode__()==unicode_text,True)
		self.assertEqual(self.author.full_name()==fullname, True)
		self.assertEqual(self.author.first_name=="rua_author_first_name", True)
		self.assertEqual(self.author.last_name=="rua_author_last_name", True)
		self.assertEqual(self.author.institution=="rua_testing", True)
		self.assertEqual(self.author.country=="GB", True)
		self.assertEqual(self.author.author_email=="fake@fakeaddress.com", True)
		self.assertEqual(self.author.full_name()==fullname, True)
		
		#alter field
		self.author.first_name="rua_changed_first_name"
		self.author.save()

		self.assertEqual(self.author.first_name=="rua_changed_first_name", True)
		#check number of created objects
		self.assertEqual(len(models.Author.objects.all())==1, True)

	def test_user_roles(self):
		user = models.User.objects.get(username="rua_user")
		roles = ["Reader","Author","Copyeditor","Reviewer","Press Editor","Book Editor","Series Editor","Indexer","Typesetter"]
		user_roles = user.profile.roles.all()
		for role in roles:
			self.assertEqual(user.profile.roles.filter(name=role).exists(), True)
		user = models.User.objects.get(username="rua_reviewer")
		roles = ["Reviewer"]
		user_roles = user.profile.roles.all()
		for role in roles:
			self.assertEqual(user.profile.roles.filter(name=role).exists(), True)
		user = models.User.objects.get(username="rua_author")
		roles = ["Author"]
		user_roles = user.profile.roles.all()
		for role in roles:
			self.assertEqual(user.profile.roles.filter(name=role).exists(), True)
		user = models.User.objects.get(username="rua_editor")
		roles = ["Press Editor","Book Editor","Series Editor"]
		user_roles = user.profile.roles.all()
		for role in roles:
			self.assertEqual(user.profile.roles.filter(name=role).exists(), True)
		user = models.User.objects.get(username="rua_onetasker")
		roles = ["Copyeditor","Indexer","Typesetter"]
		user_roles = user.profile.roles.all()
		for role in roles:
			self.assertEqual(user.profile.roles.filter(name=role).exists(), True)


	def test_book_model(self):
		"""
		test book model
		"""
		self.book = models.Book.objects.get(pk=1)
		self.book.save()
		self.author = models.Author.objects.get(pk=1)
		self.author.save()

		self.assertEqual(self.book.prefix=="rua_prefix", True)
		self.assertEqual(self.book.title=="rua_title", True)
		self.assertEqual(self.book.slug=="rua_title", True)
		self.assertEqual(self.book.subtitle=="rua_subtitle", True)
		self.assertEqual(self.book.description=="rua description", True)
		self.assertEqual(self.book.cover_letter=="cover letter", True)
		self.assertEqual(self.book.reviewer_suggestions=="reviewer suggestion", True)
		self.assertEqual(self.book.competing_interests=="competing interest", True)
		self.assertEqual(self.book.book_type=="monograph", True)
		self.assertEqual(self.book.author.filter(pk=1).exists(), True)
		self.assertEqual(self.book.subject.filter(pk=1).exists(), True)
		self.assertEqual(self.book.keywords.filter(pk=1).exists(), True)
		self.assertEqual(self.book.press_editors.filter(pk=2).exists(), True)
		self.assertEqual(self.book.license==models.License.objects.get(pk=4), True)
		self.assertEqual(self.book.owner==models.User.objects.get(pk=3), True)
		self.assertEqual(self.book.languages.filter(pk=124).exists(), True)


		#check that it exists in the database
		
		self.assertEqual(len(models.Book.objects.all())==1, True)

##############################################	View Tests	 ##############################################		

################### Dashboards ##################

	def test_editor_access(self):
		login = self.client.login(username="rua_editor", password="tester")
		resp = self.client.get(reverse('editor_dashboard'))
	
		content =resp.content
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)
	
	def test_not_editor_access(self):
		login = self.client.login(username="rua_reviewer", password="tester")
		resp = self.client.get(reverse('editor_dashboard'))
		content =resp.content
		
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, True)

	def test_editor_redirect(self):
		login = self.client.login(username="rua_editor", password="tester")
		response = self.client.get(reverse('user_dashboard'))
		self.assertRedirects(response, "http://testing/editor/dashboard/", status_code=302, target_status_code=200, host=None, msg_prefix='', fetch_redirect_response=True)

	def test_author_access(self):
		login = self.client.login(username="rua_author", password="tester")
		resp = self.client.get(reverse('author_dashboard'))
		content =resp.content
		
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)

	def test_not_author_access(self):
		login = self.client.login(username="rua_reviewer", password="tester")
		resp = self.client.get(reverse('author_dashboard'))
		content =resp.content
		self.user.last_login=timezone.now()
		self.user.save()

		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, True)

	def test_author_redirect(self):
		login = self.client.login(username="rua_author", password="tester")
		response = self.client.get(reverse('user_dashboard'))
		self.assertRedirects(response, "http://testing/author/dashboard/", status_code=302, target_status_code=200, host=None, msg_prefix='', fetch_redirect_response=True)

	def test_onetasker_access(self):
		login = self.client.login(username="rua_onetasker", password="tester")
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

	def test_onetasker_redirect(self):
		login = self.client.login(username="rua_onetasker", password="tester")
		response = self.client.get(reverse('user_dashboard'))
		self.assertRedirects(response, "http://testing/tasks/", status_code=302, target_status_code=200, host=None, msg_prefix='', fetch_redirect_response=True)
	
	def test_reviewer_access(self):
		login = self.client.login(username="rua_reviewer", password="tester")
		resp = self.client.get(reverse('reviewer_dashboard'))
		content =resp.content
		
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)

	def test_not_reviewer_access(self):
		login = self.client.login(username="rua_author", password="tester")
		resp = self.client.get(reverse('reviewer_dashboard'))
		content =resp.content
		
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, True)

	def test_reviewer_redirect(self):
		login = self.client.login(username="rua_reviewer", password="tester")
		response = self.client.get(reverse('user_dashboard'))
		self.assertRedirects(response, "http://testing/review/dashboard/", status_code=302, target_status_code=200, host=None, msg_prefix='', fetch_redirect_response=True)

	def test_view_profile(self):
		resp = self.client.get(reverse('view_profile'))
		content =resp.content
		
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)
		self.assertEqual("500" in content, False)

	def test_logout(self):
		resp = self.client.get(reverse('logout'))
		self.assertEqual(resp.status_code, 302)
		self.assertEqual(resp['Location'], "http://testing/")

	def test_login(self):
		resp = self.client.get(reverse('logout'))
		self.assertEqual(resp.status_code, 302)
		self.assertEqual(resp['Location'], "http://testing/")

		resp = self.client.post(reverse('login'),{'user_name': 'rua_user','user_pass':"root"})
		self.assertEqual(resp['Location'], "http://testing/dashboard/")
		resp = self.client.get(reverse('logout'))
	def test_login_invalid(self):
		resp = self.client.get(reverse('logout'))
		resp = self.client.post(reverse('login'),{'user_name': 'unknown','user_pass':"unknown"})
	#	resp = self.client.get(reverse('login'))
		message = self.get_specific_message(resp,1)
		self.assertEqual(str(message), 'Account not found with those details.')
	
	def test_login_not_active(self):
		resp = self.client.get(reverse('logout'))
		resp = self.client.get(reverse('register'))
		content =resp.content
		
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)	
		resp = self.client.post(reverse('register'), {'first_name': 'new','last_name':'last','username':'user1','email':'fake@faked.com','password1': 'password1','password2':"password1"})
		user = User.objects.get(username="user1")
		roles = models.Role.objects.filter(name__icontains="Editor")
		for role in roles:
			user.profile.roles.add(role)
		user.profile.save()
		user.save()
		resp = self.client.post(reverse('login'),{'user_name': 'user1','user_pass':"password1"})
		message = self.get_specific_message(resp,0)
		self.assertEqual(str(message), 'User account is not active.')
	def test_activate_user(self):
		resp = self.client.post(reverse('register'), {'first_name': 'new','last_name':'last','username':'user1','email':'fake@faked.com','password1': 'password1','password2':"password1"})
		user = User.objects.get(username="user1")
		roles = models.Role.objects.filter(name__icontains="Editor")
		for role in roles:
			user.profile.roles.add(role)
		user.profile.activation_code='activate'
		user.profile.save()
		user.save()
		resp = self.client.post(reverse('activate',kwargs={'code':'activate'}))
		self.assertEqual(resp.status_code, 302)
		self.assertEqual(resp['Location'], "http://testing/login/")
	
	def test_index(self):
		resp =  self.client.get(reverse('index'))
		self.assertEqual(resp.status_code, 302)
		self.assertEqual(resp['Location'], "http://testing/login/")
	def test_contact(self):
		resp = self.client.get(reverse('contact'))
		content =resp.content
		
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)
		self.assertEqual("Get in touch" in content, True)
		self.assertEqual("Reason" in content, True)
		self.assertEqual("Your email address" in content, True)
		self.assertEqual("Your name" in content, True)
		self.assertEqual("Your message" in content, True)
	
	def test_user_submission(self):
		login = self.client.login(username="rua_author", password="tester")
		resp = self.client.get(reverse('user_submission',kwargs={'submission_id':1}))
		content =resp.content
		
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)
		self.assertEqual("rua_title" in content, True)
		self.assertEqual("Submission Progress" in content, True)
		self.assertEqual("Summary" in content, True)
		self.assertEqual("Files" in content, True)
		self.assertEqual("Authors" in content, True)


	def test_ajax_email_calls(self):
		
		self.assertEqual(len(models.Book.objects.all())==1, True)
		self.book=models.Book.objects.get(pk=1)
		self.book.save()
		self.author=models.Author.objects.get(pk=1)
		self.author.save()

		resp =  self.client.get(reverse('get_authors',kwargs= {'submission_id':self.book.id}),{'term': 'rua',},content_type="application/json",HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		json_data =  json.loads(resp.content)
		self.assertEqual(self.author.author_email==json_data[0]["value"],True)
		resp =  self.client.get(reverse('get_editors',kwargs= {'submission_id':self.book.id}),{'term': 'rua',},content_type="application/json",HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		json_data =  json.loads(resp.content)
		editors= self.book.press_editors.all()
		self.assertEqual(editors[0].email==json_data[0]["value"],True)
		resp =  self.client.get(reverse('get_onetaskers',kwargs= {'submission_id':self.book.id}),{'term': 'rua',},content_type="application/json",HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		json_data =  json.loads(resp.content)
		onetasker= User.objects.get(pk=5)
		self.assertEqual(onetasker.email==json_data[0]["value"],True)
		resp =  self.client.get(reverse('get_all',kwargs= {'submission_id':self.book.id}),{'term': 'rua',},content_type="application/json",HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		json_data =  json.loads(resp.content)
		self.assertEqual(len(json_data)==3,True)
		resp =  self.client.get(reverse('get_all',kwargs= {'submission_id':self.book.id}),{'term': 'none_term',},content_type="application/json",HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		json_data =  json.loads(resp.content)
		self.assertEqual(len(json_data)==0,True)





##############################################	Form Tests	 ##############################################		


	def test_update_profile(self):
		resp = self.client.post(reverse('update_profile'))
		content =resp.content
		
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)
		resp = self.client.post(reverse('update_profile'), {'first_name': 'new','institution':"Testing",'country':"GB"})
		self.assertEqual(resp.status_code, 302)
		self.assertEqual(resp['Location'], "http://testing/user/profile/")

	def test_register(self):
		resp = self.client.post(reverse('register'), {'first_name': 'new','last_name':'last','username':'user1','email':'fake@faked.com','password1': 'password1','password2':"password1"})
		self.assertEqual(resp.status_code, 302)
		self.assertEqual(resp['Location'], "http://testing/login/")

	def test_reset_password(self):
		resp = self.client.post(reverse('reset_password'), {'password_1': 'password1','password_2':"password1"})
		self.assertEqual(resp.status_code, 302)
		self.assertEqual(resp['Location'], "http://testing/login/")

	def test_register_login(self):
		resp = self.client.post(reverse('register'), {'first_name': 'new','last_name':'last','username':'user1','email':'fake@faked.com','password1': 'password1','password2':"password1"})
		user = User.objects.get(username="user1")
		roles = models.Role.objects.filter(name__icontains="Editor")
		for role in roles:
			user.profile.roles.add(role)
		user.active=True
		user.save()
		user.profile.save()
		resp = self.client.post(reverse('login'),{'user_name': 'user1','user_pass':"password1"})
		self.assertEqual(resp['Location'], "http://testing/dashboard/")

############# Email

	def test_email(self):
		self.author = models.Author.objects.get(pk=1)
		self.book = models.Book.objects.get(pk=1)
		self.book.save()
		#check that it exists in the database
		
		self.assertEqual(len(models.Book.objects.all())==1, True)
		resp = self.client.post(reverse('email_users', kwargs= {'group': 'all','submission_id':str(self.book.id)}),  {'subject': 'all','to_values':self.author.author_email,"cc_values":"","bcc_values":"","body":'text'})
		self.assertEqual(resp.status_code, 200)
		self.assertEqual( "was sent" in resp.content,True)
		resp = self.client.post(reverse('email_user', kwargs= {'group': 'editors','submission_id':str(self.book.id),'user_id':self.user.id}),  {'subject': 'all','to_values':self.user.email,"cc_values":"","bcc_values":"","body":'text'})
		self.assertEqual(resp.status_code, 200)
		self.assertEqual( "was sent" in resp.content,True)





		#### Problematic ###

