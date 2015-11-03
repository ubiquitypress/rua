from django.test import TestCase
from manager import models
from django.utils import timezone
import time
import datetime
from django.test import SimpleTestCase
from django.db.models import Q
from manager import views
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
		'test_manager_data'

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

	def test_manager_users(self):
		#users page
		users = User.objects.all()
		resp = self.client.get(reverse('manager_users'))
		content =resp.content
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)
		self.assertEqual(len(users),5)
		for user in users:
			self.assertEqual(user.username in content, True)
		#add user
		resp = self.client.post(reverse('add_user'), {'username': 'rua_new_user', 'first_name': 'Usera', 'last_name': 'Lastly', 'middle_name': 'Middler', 'roles': '2', 'country': 'GB', 'email': 'fake_new_user@fakeaddress.com', 'department': 'test', 'signature': 'Hieee', 'salutation': 'Mrs','institution': 'rua_testing', 'biography': 'bio'})
		self.assertEqual(resp.status_code, 302)
		self.assertEqual(resp['Location'], "http://testing/manager/user/")
		found = False
		try:
			new_user = User.objects.get(username="rua_new_user")
			found = True
		except:
			found = False
		self.assertEqual(found, True)
		users = User.objects.all()
		self.assertEqual(len(users),6)
		#edit user
		resp = self.client.post(reverse('user_edit',kwargs={'user_id':new_user.id}),{'username': 'rua_new_user', 'first_name': 'changed', 'last_name': 'changed', 'middle_name': 'changed', 'roles': '2', 'country': 'GB', 'email': 'fake_new_user@fakeaddress.com', 'department': 'test', 'signature': 'Hieee', 'salutation': 'Mrs', 'institution': 'rua_testing', 'biography': 'bio'})
		try:
			new_user = User.objects.get(username="rua_new_user")
			found = True
		except:
			found = False
		self.assertEqual(found, True)
		self.assertEqual(new_user.first_name, "changed")
		self.assertEqual(new_user.last_name, "changed")
		self.assertEqual(new_user.profile.middle_name, "changed")

	def test_manager_roles(self):
		resp = self.client.get(reverse('manager_roles'))
		roles = core_models.Role.objects.all()
		content =resp.content
		
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)

		for role in roles:
			self.assertEqual(role.name in content, True)
			role_resp = self.client.get(reverse('manager_role',kwargs={'slug':role.slug})) #load role page
			role_content = role_resp.content
			self.assertEqual(role_resp.status_code, 200)
			self.assertEqual("403" in role_content, False)
			have_role=[]
			dont_have_role=[]
			users=User.objects.all()
			#get all users and see who has this role and who doesn't
			for user in users:
				if user.profile.roles.filter(name=role.name).exists():
					have_role.append(user)
				else:
					dont_have_role.append(user)
			#check for the users that have the role that a button exists for removing the role
			for user in have_role:
				remove_button="/manager/roles/%s/user/%s/remove/" % (role.slug,user.id)
				self.assertEqual(remove_button in role_content, True)
			#check for the users that don't have the role that a button exists for adding the role
			for user in dont_have_role:
				add_button="/manager/roles/%s/user/%s/add/" % (role.slug,user.id)
				self.assertEqual(add_button in role_content, True)

			#either remove all users from a role or add them all
			expected_size=len(have_role)+len(dont_have_role)
			if len(have_role)>0:
				for user in have_role:
					remove = self.client.post(reverse('manager_role_action',kwargs={'slug':role.slug,'user_id':user.id,'action':'remove'}))

			elif len(dont_have_role)>0:				
				for user in dont_have_role:
					add = self.client.post(reverse('manager_role_action',kwargs={'slug':role.slug,'user_id':user.id,'action':'add'}))
			
			
			role_resp = self.client.get(reverse('manager_role',kwargs={'slug':role.slug}))
			role_content = role_resp.content
			self.assertEqual(role_resp.status_code, 200)
			self.assertEqual("403" in role_content, False)
			have_role=[]
			dont_have_role=[]
			users=User.objects.all()
			#recreate lists
			for user in users:
				if user.profile.roles.filter(name=role.name).exists():
					have_role.append(user)
				else:
					dont_have_role.append(user)
			# check which list has all the users and check that the buttons exist for removing or adding the roles 
			if len(dont_have_role)>0:
				self.assertEqual(len(dont_have_role),expected_size)
				for user in dont_have_role:
					add_button="/manager/roles/%s/user/%s/add/" % (role.slug,user.id)
					self.assertEqual(add_button in role_content, True)
			else:
				self.assertEqual(len(have_role),expected_size)
				for user in have_role:
					remove_button="/manager/roles/%s/user/%s/remove/" % (role.slug,user.id)
					self.assertEqual(remove_button in role_content, True)

	def test_manager_groups(self):
		resp = self.client.get(reverse('manager_groups'))
		groups = models.Group.objects.all()
		content =resp.content
		
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)
		for group in groups:
			self.assertEqual(group.name in content, True)
		found = False
		resp = self.client.post(reverse('manager_group_add'),{'group_type': 'generic', 'name': 'rua_new_group', 'active': True, 'sequence': 4})
		try:
			new_group = models.Group.objects.get(name="rua_new_group")
			found = True
		except:
			found = False
		self.assertEqual(found, True)

		found = False
		resp = self.client.post(reverse('manager_group_edit',kwargs={'group_id':4}),{'group_type': 'generic', 'name': 'changed_name', 'active': True, 'sequence': 4})

		try:
			new_group = models.Group.objects.get(name="changed_name")
			found = True
		except:
			found = False
		self.assertEqual(found, True)
		found = False
		resp = self.client.post(reverse('manager_group_delete',kwargs={'group_id':4}))
		try:
			new_group = models.Group.objects.get(name="changed_name")
			found = True
		except:
			found = False
		self.assertEqual(found, False)
		editorial_group = models.Group.objects.get(name="rua_editorial_group")
		editorial_group_members = models.GroupMembership.objects.filter(group=editorial_group)
		self.assertEqual(len(editorial_group_members),2)

		resp = self.client.get(reverse('manager_group_members',kwargs={'group_id':editorial_group.id}))
		content =resp.content
		
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)
		for member in editorial_group_members:
			self.assertEqual(member.user.first_name in content, True)
			self.assertEqual(member.user.last_name in content, True)
			remove_button = "/manager/groups/%s/members/%s/delete" % (editorial_group.id,member.id)
			self.assertEqual(remove_button in content, True)
		resp = self.client.post(reverse('manager_membership_delete',kwargs={'group_id':editorial_group.id,'member_id':1}))
		editorial_group_members = models.GroupMembership.objects.filter(group=editorial_group)
		self.assertEqual(len(editorial_group_members),1)
		new_user=User.objects.get(username="rua_reviewer")
		resp = self.client.post(reverse('group_members_assign',kwargs={'group_id':editorial_group.id,'user_id':new_user.id}))
		editorial_group_members = models.GroupMembership.objects.filter(group=editorial_group)
		self.assertEqual(len(editorial_group_members),2)

	def test_manager_settings(self):
		resp = self.client.get(reverse('settings_index'))
		content =resp.content
		
		self.assertEqual(resp.status_code, 200)
		self.assertEqual("403" in content, False)
		groups =core_models.SettingGroup.objects.all()
		for group in groups:
			self.assertEqual(group.name.title() in content, True)
			settings = core_models.Setting.objects.filter(group=group)
			for setting in settings:
				self.assertEqual(setting.name in content, True)
				setting_resp = self.client.get(reverse('edit_setting',kwargs={'setting_group':group.name,'setting_name':setting.name}))
				self.assertEqual(setting_resp.status_code, 200)
				setting_content=setting_resp.content
				self.assertEqual("403" in setting_content, False)
				self.assertEqual("Submit" in setting_content, True)
				self.assertEqual('name="value"' in setting_content, True)
				self.assertEqual("Delete" in setting_content, True)
		setting=core_models.Setting.objects.get(name="remind_accepted_reviews")
		self.assertEqual(setting.value,str(7))
		self.client.post(reverse('edit_setting',kwargs={'setting_group':group.name,'setting_name':setting.name}),{'value':8})
		setting=core_models.Setting.objects.get(name="remind_accepted_reviews")
		self.assertEqual(setting.value,str(8))












	





		


