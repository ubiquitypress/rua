from django.test import TestCase
from core import models
from django.utils import timezone
import time
import datetime
from core import views
from django.http import HttpRequest
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import resolve, reverse

# Create your tests here.

class CoreTests(TestCase):

	# Dummy DBs
	fixtures = [
		'settinggroups',
		'settings',
		'langs',
		'cc-licenses',
		'role',
	]

	def setUp(self):
		self.client = Client()
		self.username = 'rua_user'
		self.email = 'fake.emaill@fakeaddress.com'
		self.password = 'rua_tester'
		self.user = User.objects.create_user(username=self.username, email=self.email,first_name="Rua",last_name="Testing", password=self.password)
		self.profile=models.Profile(user=self.user,institution="Testing",country="GB",department="test")
		login = self.client.login(username='rua_user', password='rua_tester')
		self.assertEqual(login, True)

	def tearDown(self):
		pass

	def test_set_up(self):
		"""
		testing set up
		"""
		self.assertEqual(self.user.username=="rua_user", True)
		self.assertEqual(self.user.email=="fake.emaill@fakeaddress.com", True)
		self.assertEqual(self.user.first_name=="Rua", True)
		self.assertEqual(self.user.last_name=="Testing", True)
		self.assertEqual(self.user.profile.institution=="Testing", True)
		self.assertEqual(self.user.profile.country=="GB", True)
		self.assertEqual(self.user.profile.department=="test", True)

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
