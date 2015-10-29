from django.test import TestCase
from django.core.urlresolvers import resolve, reverse
from django.test.client import Client
from django.contrib.auth.models import User
from django.contrib import messages

class EditorTests(TestCase):

    # Dummy DBs
    fixtures = [
    	'auth',
        'core',
        'tasks',
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
        login = self.client.login(username='andy', password='legosword12')
        self.assertEqual(login, True)

    def tearDown(self):
        pass

    def test_editor_dashboard(self):
        """Fetches the editor dashboard"""
        resp = self.client.get(reverse('editor_dashboard'))
        self.assertTrue(resp.status_code, 200)
        self.assertContains(resp, "Subtitle")

    def test_editor_dashboard_filter(self):
    	"""Tests out the filters on the Editor Dashboard"""
    	resp = self.client.post(reverse('editor_dashboard'), {'filter': 'review', 'order': 'title'})
    	self.assertTrue(resp.status_code, 200)
    	self.assertContains(resp, "Book 42: Prefix Title Subtitle")
    	self.assertNotContains(resp, "Book 45: Armed Services Unit Are they valuable?")


