from datetime import date

from django.test import TestCase
from core import models as core_models
from core import logic as core_logic
from django.test.client import Client
from django.contrib.auth.models import User
from django.urls import reverse


class OnetaskerTests(TestCase):
    # Dummy DBs
    fixtures = [
        'settinggroups',
        'settings/master',
        'langs',
        'cc-licenses',
        'role',
        'test/test_auth_data',
        'test/test_review_data',
        'test/test_core_data',
        'test/test_index_assignment_data',
        'test/test_copyedit_assignment_data',

    ]

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username="rua_onetasker")
        self.user.save()
        self.book = core_models.Book.objects.get(pk=1)

        login = self.client.login(username="rua_onetasker", password="tester")
        self.assertTrue(login)

    def tearDown(self):
        pass

    def test_set_up(self):
        """
        testing set up
        """
        self.assertEqual(self.user.username == "rua_onetasker", True)
        self.assertEqual(self.user.email == "fake_onetasker@fakeaddress.com",
                         True)
        self.assertEqual(self.user.first_name == "rua_onetasker_first_name",
                         True)
        self.assertEqual(self.user.last_name == "rua_onetasker_last_name", True)
        self.assertEqual(self.user.profile.institution == "rua_testing", True)
        self.assertEqual(self.user.profile.country == "GB", True)

    def test_onetasker_access(self):
        resp = self.client.get(reverse('onetasker_dashboard'))
        content = resp.content

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b"403" in content, False)

    def test_not_onetasker_access(self):
        self.client.login(username="rua_reviewer", password="tester")
        resp = self.client.get(reverse('onetasker_dashboard'))
        content = resp.content

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b"403" in content, True)

    def test_onetasker_dashboard(self):
        response = self.client.get(reverse('user_dashboard'))
        self.assertRedirects(
            response, "/tasks/",
            status_code=302,
             target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )
        onetasker_tasks = core_logic.onetasker_tasks(self.user)
        active_count = len(onetasker_tasks.get('active'))
        self.assertEqual(active_count, 3)
        response = self.client.get(reverse('onetasker_dashboard'))
        content = response.content
        self.assertEqual(response.status_code, 200)
        self.assertEqual(b"403" in content, False)
        self.assertEqual(b"Copyedit" in content, True)
        self.assertEqual(b"Indexing" in content, True)
        self.assertEqual(b"Typesetting" in content, True)
        self.assertEqual(b"rua_title" in content, True)

    def test_onetasker_tasks(self):
        onetasker_tasks = core_logic.onetasker_tasks(self.user)
        active_tasks = onetasker_tasks.get('active')

        for task in active_tasks:
            # decision page
            response = self.client.get(reverse('onetasker_task_hub', kwargs={
                'assignment_type': task.get('type'),
                'assignment_id': task.get('assignment').id}))
            content = response.content
            self.assertEqual(response.status_code, 200)
            self.assertEqual(b"403" in content, False)
            self.assertTrue(b"You can accept or reject this task" in content)
            self.assertEqual(b"I Accept" in content, True)
            self.assertEqual(b"I Decline" in content, True)

            # about/submission details page
            assignment = task.get('assignment')
            book = assignment.book
            authors = book.author.all()

            response = self.client.get(
                reverse('onetasker_task_about',
                        kwargs={'assignment_type': task.get('type'),
                                'assignment_id': assignment.id,
                                'about': 'about'}
                        )
            )
            content = response.content
            self.assertEqual(b"AUTHORS" in content, True)
            for author in authors:
                self.assertIn(bytes(author.full_name(), 'utf-8'), content)
            self.assertIn(b"DESCRIPTION", content)
            self.assertIn(bytes(book.description, 'utf-8'), content)

            ### decision - accept
            response = self.client.post(
                reverse(
                    'onetasker_task_hub',
                    kwargs={
                        'assignment_type': task.get('type'),
                        'assignment_id': assignment.id
                    }
                ),
                {'decision': 'accept'}
            )
            self.assertEqual(response.status_code, 302)
            self.assertEqual(
                response['Location'],
                "/tasks/{task_type}/{assignment_id}".format(
                    task_type=task.get('type'),
                    assignment_id=assignment.id
                )
            )
            assignment.refresh_from_db()
            self.assertEqual(assignment.accepted, date.today())

            # task page
            response = self.client.get(
                reverse('onetasker_task_hub',
                        kwargs={'assignment_type': task.get('type'),
                                'assignment_id': task.get('assignment').id})
            )
            content = response.content
            self.assertEqual(response.status_code, 200)
            self.assertEqual(b"403" in content, False)
            # Manual formatting to match the date rendered by the template
            message = 'You accepted on ' + '{:%d %b %G}'.format(
                assignment.accepted
            ).lstrip('0')
            self.assertIn(bytes(message, 'utf-8'), content)

            ### decision - decline
            assignment.accepted = None
            assignment.save()
            response = self.client.post(
                reverse(
                    'onetasker_task_hub',
                    kwargs={
                        'assignment_type': task.get('type'),
                        'assignment_id': task.get('assignment').id
                    }
                ),
                {'decision': 'decline'}
            )
            self.assertEqual(response.status_code, 302)
            self.assertEqual(
                response['Location'],
                "/tasks/{task_type}/1/decline/".format(
                    task_type=task.get('type')
                )
            )

            response = self.client.get(
                reverse('onetasker_task_hub_decline',
                        kwargs={
                            'assignment_type': task.get('type'),
                           'assignment_id': task.get('assignment').id})
            )
            self.assertEqual(response.status_code, 200)

            response = self.client.post(
                reverse('onetasker_task_hub_decline',
                        kwargs={'assignment_type': task.get('type'),
                                'assignment_id': task.get('assignment').id}),
                {'decline-email': 'decline'}
            )
            self.assertEqual(response.status_code, 302)
