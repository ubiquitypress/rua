import tempfile
import datetime

from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.test.client import Client
from django.contrib.auth.models import User
from django.utils import timezone
from core import models as core_models
import logging

from revisions import models as revision_models
from editor import logic

LOG = logging.getLogger(__name__)


class EditorTests(TestCase):
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
        'test/test_manager_data',
        'test/test_submission_checklist_item_data',
        'test/test_proposal_form',
        'test/test_contract_data',
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
        self.superuser = User.objects.get(username="rua_editor")
        self.editor_user = User.objects.get(username="rua_editor")
        self.book = core_models.Book.objects.get(pk=1)
        self.chapter = core_models.Chapter.objects.get(pk=1)
        self.chapter_authors = core_models.ChapterAuthor.objects.filter(
            chapter=self.chapter)
        self.factory = RequestFactory()
        login = self.client.login(username='rua_editor', password='tester')
        self.assertEqual(login, True)

    def tearDown(self):
        pass

    def test_editor_dashboard(self):
        """Fetches the editor dashboard"""
        resp = self.client.get(reverse('editor_dashboard'))
        content = resp.content
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(b"403" in content)
        self.assertContains(
            resp,
            "Book {book_id} - {book_prefix}"
            " {book_title}: {book_subtitle}".format(
                book_id=self.book.id,
                book_prefix=self.book.prefix,
                book_title=self.book.title,
                book_subtitle=self.book.subtitle
            )
        )

    def test_editor_dashboard_filter(self):
        """Tests out the filters on the Editor Dashboard"""
        self.book.stage.current_stage = 'submission'
        self.book.stage.review = None
        self.book.stage.save()
        self.book.save()

        resp = self.client.post(
            reverse('editor_dashboard'),
        {'filter': 'review',
         'order': 'title',
         'search': 'rua'})
        content = resp.content
        self.assertTrue(resp.status_code, 200)
        self.assertNotContains(
            resp,
            "Book {book_id} - {book_prefix}"
            " {book_title}: {book_subtitle}".format(
                book_id=self.book.id,
                book_prefix=self.book.prefix,
                book_title=self.book.title,
                book_subtitle=self.book.subtitle)
        )

    def test_submission(self):
        self.book.stage.current_stage = 'submission'
        self.book.stage.review = None
        self.book.stage.save()
        self.book.save()
        book = core_models.Book.objects.get(pk=1)
        self.assertEqual(book.stage.current_stage == 'submission', True)

        resp = self.client.get(
            reverse('editor_submission',
                    kwargs={'submission_id': self.book.id})
        )
        content = resp.content
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b"403" in content, False)
        self.assertEqual(b"AUTHORS" in content, True)
        authors = self.book.author.all()
        for author in authors:
            self.assertEqual(
                bytes(author.full_name(), 'utf-8') in content,
                True
            )
        self.assertEqual(b"COVER LETTER" in content, True)
        self.assertEqual(
            bytes(self.book.cover_letter, 'utf-8') in content,
            True
        )
        self.assertEqual(b"REVIEWER SUGGESTIONS" in content, True)
        self.assertEqual(
            bytes(self.book.reviewer_suggestions, 'utf-8') in content,
            True
        )
        self.assertEqual(b"COMPETING INTERESTS" in content, True)
        self.assertEqual(
            bytes(self.book.competing_interests, 'utf-8') in content,
            True
        )

        resp = self.client.post(
            reverse(
                'editor_decision',
                kwargs={
                    'submission_id': self.book.id,
                    'decision': 'review'
                }
            ),
            {'decision': 'review'}
        )
        book = core_models.Book.objects.get(pk=1)
        self.assertEqual(book.stage.current_stage, 'review')

    def test_submission_status(self):
        resp = self.client.get(
            reverse('editor_status', kwargs={'submission_id': self.book.id}))
        content = resp.content
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b"403" in content, False)
        self.assertEqual(b"Current Status" in content, True)
        self.assertEqual(b"Submission Progress" in content, True)
        self.assertEqual(b"Review" in content, True)
        self.assertEqual(b"Submission" in content, True)

    def test_submission_decline(self):
        resp = self.client.post(reverse('editor_decline_submission',
                                        kwargs={'submission_id': self.book.id}),
                                {'decline': ''})
        book = core_models.Book.objects.get(pk=1)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp['Location'], "/editor/dashboard/")
        self.assertEqual(book.stage.current_stage, 'declined')

    def test_submission_contract(self):
        resp = self.client.get(
            reverse('contract_manager',
                    kwargs={'submission_id': self.book.id})
        )
        content = resp.content
        book = core_models.Book.objects.get(pk=1)
        contracts = core_models.Contract.objects.all()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b"403" in content, False)
        self.assertEqual(len(contracts), 1)
        self.assertEqual(book.contract, None)
        self.assertTrue(b"Upload  Contract" in content)
        self.assertFalse(b"Contract Info" in content)

        self.book.contract = core_models.Contract.objects.get(pk=1)
        self.book.save()
        resp = self.client.get(
            reverse('contract_manager',
                    kwargs={'submission_id': self.book.id})
        )
        content = resp.content
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b"403" in content, False)
        self.assertEqual(b"Contract Info" in content, True)
        self.assertEqual(b"test_contract" in content, True)

        resp = self.client.get(
            reverse('contract_manager_edit',
            kwargs={'submission_id': self.book.id,
                   'contract_id': 1})
        )
        content = resp.content
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b"403" in content, False)
        self.assertEqual(b"Update  Contract" in content, True)
        self.assertEqual(b"test_contract" in content, True)

        resp = self.client.post(
            reverse('contract_manager_edit',
                    kwargs={'submission_id': self.book.id,
                            'contract_id': 1}),
            {'title': 'updated_title', 'notes': 'notes',
             'editor_signed_off': '2015-11-11',
             'author_signed_off': '2015-11-23'}
        )
        contract = core_models.Contract.objects.get(pk=1)
        self.assertEqual(contract.title == "updated_title", True)

    def test_submission_tasks(self):
        resp = self.client.get(
            reverse('editor_tasks', kwargs={'submission_id': self.book.id}))
        content = resp.content
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b"403" in content, False)
        self.assertEqual(b"My Tasks" in content, True)
        self.assertEqual(b"No outstanding tasks" in content, True)
        self.typeset_assignment = core_models.TypesetAssignment.objects.get(
            pk=1)
        self.typeset_assignment.accepted = timezone.now()
        self.typeset_assignment.requestor = self.superuser
        self.typeset_assignment.author_invited = timezone.now()
        self.typeset_assignment.author_completed = timezone.now()
        self.typeset_assignment.save()
        resp = self.client.get(
            reverse('editor_tasks', kwargs={'submission_id': self.book.id}))
        content = resp.content
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b"403" in content, False)
        self.assertEqual(b"My Tasks" in content, True)
        self.assertEqual(b"No outstanding tasks" in content, False)
        self.assertEqual(b"Typesetting Review" in content, True)

    def test_editor_review_round_cancel(self):
        book = core_models.Book.objects.get(pk=1)
        self.assertEqual(book.stage.current_stage == 'review', True)
        rounds = core_models.ReviewRound.objects.all()
        self.assertEqual(rounds.count(), 1)
        LOG.warn(
            "possibly modifying server state with GET requests."
            " this is a really bad idea")
        self.client.get(
            reverse('editor_review_round_cancel',
                    kwargs={'submission_id': self.book.id,
                            'round_number': 1})
        )
        rounds = core_models.ReviewRound.objects.all()
        self.assertEqual(rounds.count(), 0)

    def test_editor_review_review_round(self):
        self.assertEqual(self.book.stage.current_stage, 'review')

        resp = self.client.get(
            reverse(
                'editor_review',
                kwargs={
                    'submission_id': self.book.id
                }
            )
        )
        content = resp.content
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b"403" in content, False)
        resp = self.client.post(
            reverse(
                'editor_review',
                kwargs={
                    'submission_id': self.book.id
                }
            ),
            {'new_round': ''}
        )

        resp = self.client.get(
            reverse(
                'editor_review',
                kwargs={
                    'submission_id': self.book.id
                }
            )
        )
        content = resp.content
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b"403" in content, False)
        self.assertEqual(b"btn-task" in content, True)

        resp = self.client.get(
            reverse(
                'editor_review_round',
                kwargs={
                    'round_number': 1,
                    'submission_id': self.book.id
                }
            )
        )
        content = resp.content
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b"403" in content, False)
        self.assertEqual(b"btn-task" in content, True)
        self.assertEqual(b"ROUND 1" in content, True)
        review_file = tempfile.NamedTemporaryFile(delete=False, suffix='.docx')

        resp = self.client.get(
            reverse(
                'editor_add_reviewers',
                kwargs={
                    'round_number': 1,
                    'submission_id': self.book.id,
                    'review_type': 'internal'
                }
            )
        )
        content = resp.content
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b"403" in content, False)

        # Delete all review assignments
        # The below request creates a duplicate
        # of an assignment described in the fixture test/test_core_data
        for review_assignment in core_models.ReviewAssignment.objects.all():
            review_assignment.delete()
        resp = self.client.post(
            reverse(
                'editor_add_reviewers',
                kwargs={
                    'round_number': 1,
                    'submission_id': self.book.id,
                    'review_type': 'internal'
                }
            ),
            {
                'message': 'Dear reviewer',
                'due_date': '2015-11-11',
                'review_form': 'rua_test_form',
                'committee': 2,
                'reviewer': 4,
                'attachment': review_file
            }
        )
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(
            resp['Location'],
            "/editor/submission/1/review/round/2/"
        )

        resp = self.client.get(
            reverse(
                'editor_add_reviewers',
                kwargs={
                        'round_number': 1,
                        'submission_id': self.book.id,
                        'review_type': 'external'
                }
            )
        )
        content = resp.content
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b"403" in content, False)

        resp = self.client.post(
            reverse(
                'editor_add_reviewers',
                kwargs={
                    'round_number': 1,
                    'submission_id': self.book.id,
                    'review_type': 'external'
                }
            ),
            {
                'message': 'Dear reviewer',
                'due_date': '2015-11-11',
                'review_form': 'rua_test_form',
                'committee': 2,
                'reviewer': 4,
                'attachment': review_file
            }
        )
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(
            resp['Location'],
            "/editor/submission/1/review/round/2/"
        )

        assignment = core_models.ReviewAssignment.objects.filter(
            book=self.book,
            review_round=1,
            review_type='external'
        )[0]

        resp = self.client.get(
            reverse(
                'update_review_due_date',
                kwargs={
                    'round_id': 1,
                    'submission_id': self.book.id,
                    'review_id': assignment.id
                }
            )
        )
        content = resp.content
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b"403" in content, False)
        resp = self.client.post(
            reverse(
                'update_review_due_date',
                kwargs={
                    'round_id': 1,
                    'submission_id': self.book.id,
                    'review_id': assignment.id
                }
            ),
            {'due_date': '2015-11-24'}
        )
        assignment = core_models.ReviewAssignment.objects.get(pk=assignment.id)
        self.assertEqual('2015-11-24', assignment.due.strftime("%Y-%m-%d"))

        resp = self.client.get(
            reverse(
                'add_review_files',
                kwargs={
                    'submission_id': self.book.id,
                    'review_type': 'internal'
                }
            )
        )
        content = resp.content
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b"403" in content, False)

        resp = self.client.post(
            reverse(
                'add_review_files',
                kwargs={
                    'submission_id': self.book.id,
                    'review_type': 'internal'
                }
            ),
            {'file': 2}
        )
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(
            resp['Location'],
            "/editor/submission/1/review/round/2/"
        )

        resp = self.client.post(
            reverse(
                'add_review_files',
                kwargs={
                    'submission_id': self.book.id,
                    'review_type': 'external'
                }
            ),
            {'file': 2}
        )
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(
            resp['Location'],
            "/editor/submission/1/review/round/2/"
        )

        resp = self.client.post(
            reverse(
                'delete_review_files',
                kwargs={
                    'submission_id': self.book.id,
                    'review_type': 'external',
                    'file_id': 2
                }
            )
        )
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(
            resp['Location'],
            "/editor/submission/1/review/round/2/"
        )
        resp = self.client.post(
            reverse(
                'delete_review_files',
                kwargs={
                    'submission_id': self.book.id,
                    'review_type': 'internal',
                    'file_id': 2
                }
            )
        )
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(
            resp['Location'],
            "/editor/submission/1/review/round/2/"
        )

        removed_file = core_models.File.objects.get(pk=2)
        self.assertNotIn(removed_file, self.book.internal_review_files.all())

    def test_published_books(self):
        resp = self.client.get(reverse('editor_published_books'))
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(b"403" in resp.content)
        self.assertTrue(b"Published Submissions" in resp.content)

    def test_editor_add_editors(self):
        book = core_models.Book.objects.get(pk=1)
        resp = self.client.get(
            reverse('editor_add_editors', kwargs={'submission_id': 1}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b"403" in resp.content, False)
        self.assertEqual(len(book.book_editors.all()), 0)

        resp = self.client.get(
            reverse(
                'editor_add_editors',
                kwargs={'submission_id': 1}),
            {'add': 1}
        )
        book = core_models.Book.objects.get(pk=1)
        self.assertEqual(len(book.book_editors.all()), 1)
        resp = self.client.get(
            reverse(
                'editor_add_editors',
                kwargs={'submission_id': 1}),
            {'remove': 1}
        )
        book = core_models.Book.objects.get(pk=1)
        self.assertEqual(len(book.book_editors.all()), 0)

    def test_editor_change_owner(self):
        book = core_models.Book.objects.get(pk=1)
        self.assertEqual(book.owner, User.objects.get(pk=3))
        resp = self.client.get(
            reverse('editor_add_editors', kwargs={'submission_id': 1}),
            {'add': 2})
        resp = self.client.get(
            reverse('editor_change_owner', kwargs={'submission_id': 1}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b"403" in resp.content, False)
        resp = self.client.get(
            reverse('editor_change_owner', kwargs={'submission_id': 1}),
            {'user': 2})
        book = core_models.Book.objects.get(pk=1)
        self.assertEqual(book.owner, User.objects.get(pk=2))
        resp = self.client.get(
            reverse(
                'editor_change_owner',
                kwargs={'submission_id': 1}),
            {'author': 1}
        )
        book = core_models.Book.objects.get(pk=1)
        author = core_models.Author.objects.get(pk=1)
        self.assertEqual(book.owner.first_name, author.first_name)
        self.assertEqual(book.owner.last_name, author.last_name)
        self.assertEqual(book.owner.email, author.author_email)

    def test_editor_notes(self):
        resp = self.client.get(
            reverse('editor_notes', kwargs={'submission_id': 1}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b"403" in resp.content, False)
        notes = core_models.Note.objects.all()
        self.assertEqual(notes.count(), 0)

        resp = self.client.get(
            reverse('editor_notes_add',
                    kwargs={'submission_id': 1})
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b"403" in resp.content, False)

        resp = self.client.post(
            reverse('editor_notes_add',
                    kwargs={"submission_id": 1}),
            {"text": "note_test"}
        )
        notes = core_models.Note.objects.all()
        self.assertEqual(notes.count(), 1)

        resp = self.client.get(
            reverse('editor_notes_view',
                kwargs={
                    "submission_id": 1,
                    "note_id": 1
                }
            )
        )
        content = resp.content
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b"403" in content, False)

        resp = self.client.get(
            reverse('editor_notes_update',
                    kwargs={"submission_id": 1,
                            "note_id": 1})
        )
        content = resp.content
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b"403" in content, False)

        resp = self.client.post(
            reverse('editor_notes_update',
                    kwargs={"submission_id": 1,
                            "note_id": 1}),
            {"text": "note_test"}
        )
        content = resp.content
        self.assertEqual(b"403" in content, False)

    def test_editor_editing(self):
        resp = self.client.post(
            reverse('editor_decision',
                    kwargs={'submission_id': self.book.id,
                            'decision': 'editing'}),
            {'decision': 'editing'}
        )
        book = core_models.Book.objects.get(pk=1)
        self.assertEqual(book.stage.current_stage == 'editing', True)

        resp = self.client.get(
            reverse('editor_editing', kwargs={'submission_id': self.book.id}))
        content = resp.content
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b"403" in content, False)
        self.assertEqual(b"COPYEDITING" in content, True)
        self.assertEqual(b"INDEXING" in content, True)
        self.assertEqual(b"Stage has not been initialised." in content, True)
        self.book.stage.copyediting = timezone.now()
        self.book.stage.indexing = timezone.now()
        self.book.stage.save()
        self.book.save()

        resp = self.client.get(
            reverse('editor_editing',
                    kwargs={'submission_id': self.book.id})
        )
        content = resp.content
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b"403" in content, False)
        self.assertEqual(b"COPYEDITING" in content, True)
        self.assertEqual(b"INDEXING" in content, True)
        self.assertEqual(b"Stage has not been initialised." in content, False)

        resp = self.client.get(
            reverse('assign_indexer', kwargs={'submission_id': book.id}))
        content = resp.content
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b"403" in content, False)

        resp = self.client.post(
            reverse('assign_indexer',
                    kwargs={'submission_id': book.id}),
            {'due_date': '2016-04-21',
             'indv-reviewer_length': ['5'],
             'copyeditor': ['5'],
             'attachment_file': '',
             'note': 'Note',
             'file': ['4'],
             'assignment-files_length': ['5'],
             'message': 'Dear'}
        )
        content = resp.content
        self.assertEqual(resp.status_code, 302)

        resp = self.client.get(
            reverse('assign_copyeditor',
                    kwargs={'submission_id': book.id})
        )
        content = resp.content
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b"403" in content, False)
        self.assertEqual(core_models.CopyeditAssignment.objects.count(), 0)

        resp = self.client.post(
            reverse('assign_copyeditor',
                    kwargs={'submission_id': book.id}),
            {'due_date': '2016-04-21',
             'indv-reviewer_length': ['5'],
             'copyeditor': ['5'],
             'attachment_file': [''],
             'note': 'Note',
             'file': ['4'],
             'assignment-files_length': ['5'],
             'message': 'Dear'}
        )
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(core_models.CopyeditAssignment.objects.count(), 1)
        new_assignment = core_models.CopyeditAssignment.objects.first()
        onetasker = User.objects.get(username="rua_onetasker")

        resp = self.client.get(
            reverse('view_copyedit',
                    kwargs={
                        'copyedit_id': new_assignment.id,
                        'submission_id': self.book.id
                    })
        )
        content = resp.content
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b"403" in content, False)
        self.assertEqual(b"COPYEDITING" in content, True)
        self.assertEqual(b"INDEXING" in content, True)
        self.assertEqual(b"Stage has not been initialised." in content, False)
        title = "COPYEDITING: {first_name} {last_name}".format(
            first_name=onetasker.first_name.upper(),
            last_name=onetasker.last_name.upper()
        )
        self.assertEqual(bytes(title, encoding='utf-8') in content, True)

        resp = self.client.get(
            reverse('view_index',
                    kwargs={
                        'index_id': 1,
                        'submission_id': self.book.id
                    })
        )
        content = resp.content
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b"403" in content, False)
        self.assertEqual(b"COPYEDITING" in content, True)
        self.assertEqual(b"INDEXING" in content, True)
        self.assertEqual(b"Stage has not been initialised." in content, False)
        title = "INDEXING: %s %s" % (
            onetasker.first_name.upper(), onetasker.last_name.upper())
        self.assertEqual(bytes(title, 'utf-8') in content, True)

    def test_editor_production(self):
        self.book.stage.current_stage = 'production'
        self.book.stage.production = timezone.now()
        self.book.stage.save()
        self.book.save()
        resp = self.client.get(reverse('editor_production',
                                       kwargs={'submission_id': self.book.id}))
        content = resp.content
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b"403" in content, False)
        self.assertEqual(b"Typesetting" in content, True)
        self.assertEqual(b"Stage has not been initialised." in content, True)
        self.book.stage.typesetting = timezone.now()
        self.book.stage.save()
        self.book.save()
        resp = self.client.get(reverse('editor_production',
                                       kwargs={'submission_id': self.book.id}))
        content = resp.content
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b"403" in content, False)
        self.assertEqual(b"Typesetting" in content, True)
        self.assertEqual(b"Stage has not been initialised." in content, False)

        resp = self.client.get(reverse('view_typesetter',
                                       kwargs={'typeset_id': 1,
                                               'submission_id': self.book.id}))
        content = resp.content
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b"403" in content, False)
        self.assertEqual(b"Typesetting" in content, True)
        self.assertEqual(b"Stage has not been initialised." in content, False)
        onetasker = User.objects.get(username="rua_onetasker")
        title = "TYPESETTING: %s %s" % (
            onetasker.first_name.upper(), onetasker.last_name.upper())
        self.assertEqual(bytes(title, 'utf-8') in content, True)

    def test_editor_publish(self):
        resp = self.client.post(
            reverse('editor_review', kwargs={'submission_id': self.book.id}),
            {'move_to_editing': ''})
        self.book.stage.current_stage = 'production'
        self.book.stage.production = timezone.now()
        self.book.stage.save()
        self.book.save()
        resp = self.client.post(
            reverse('editor_publish', kwargs={'submission_id': self.book.id}))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(
            resp['Location'],
            "/editor/submission/1/"
        )

        book = core_models.Book.objects.get(pk=1)
        self.assertEqual(book.stage.current_stage == 'published', True)

    def test_request_revisions(self):
        resp = self.client.get(reverse('request_revisions',
                                       kwargs={'submission_id': self.book.id,
                                               'returner': 'review'}))
        content = resp.content
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b"403" in content, False)
        resp = self.client.post(reverse('request_revisions',
                                        kwargs={'submission_id': self.book.id,
                                                'returner': 'review'}),
                                {'notes_from_editor': 'notes',
                                 'due': '2015-11-30',
                                 'id_email_text': 'Hi User'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp['Location'],
                         "/editor/submission/1/review/")
        self.client.login(username="rua_author", password="tester")
        revision = revision_models.Revision.objects.get(book=self.book)
        resp = self.client.post(reverse('author_revision',
                                        kwargs={'submission_id': self.book.id,
                                                'revision_id': revision.id}),
                                {'cover_letter': 'updated cover letter'})
        self.client.login(username="rua_editor", password="tester")
        resp = self.client.get(reverse('editor_dashboard'))
        content = resp.content
        self.assertTrue(resp.status_code, 200)
        self.assertEqual(b"403" in content, False)
        notification = "Revisions submitted for %s" % self.book.title
        self.assertEqual(bytes(notification, 'utf-8') in content, True)
        resp = self.client.get(
            reverse(
                'editor_view_revisions',
                kwargs={
                    'submission_id': self.book.id,
                    'revision_id': revision.id
                }
            )
        )
        content = resp.content
        self.assertTrue(resp.status_code, 200)
        self.assertEqual(b"403" in content, False)

    def test_catalog(self):
        resp = self.client.get(
            reverse('catalog', kwargs={'submission_id': self.book.id}))
        content = resp.content
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b"403" in content, False)
        self.assertEqual(b"Prefix" in content, True)
        self.assertEqual(b"Title" in content, True)
        self.assertEqual(b"Subtitle" in content, True)
        self.assertEqual(b"Series" in content, True)
        self.assertEqual(b"License" in content, True)
        self.assertEqual(b"Pages" in content, True)
        self.assertEqual(b"Slug" in content, True)
        self.assertEqual(b"Review type" in content, True)
        self.assertEqual(b"Publication date" in content, True)
        self.assertEqual(b"Languages" in content, True)
        self.assertEqual(b"Abstract" in content, True)
        self.assertEqual(b"Keywords" in content, True)
        resp = self.client.get(
            reverse('identifiers', kwargs={'submission_id': self.book.id}))
        content = resp.content
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b"403" in content, False)
        self.assertEqual(b"Identifier" in content, True)
        self.assertEqual(b"Digital format" in content, True)
        self.assertEqual(b"Physical format" in content, True)
        self.assertEqual(b"Value" in content, True)
        self.assertEqual(b"Use the form to add a new identifier." in content,
                         True)
        resp = self.client.post(
            reverse('identifiers', kwargs={'submission_id': self.book.id}),
            {'identifier': 'doi', 'digital_format': '', 'physical_format': '',
             'value': 1, 'displayed': True})
        identifiers = core_models.Identifier.objects.all()
        self.assertEqual(len(identifiers), 1)
        resp_get = self.client.get(
            reverse('identifiers', kwargs={'submission_id': self.book.id}))
        content = resp_get.content
        self.assertEqual(resp_get.status_code, 200)
        self.assertEqual(b"403" in content, False)
        self.assertEqual(b"Use the form to add a new identifier." in content,
                         False)
        self.assertEqual(
            b"/editor/submission/1/catalog/identifiers/1/" in content, True)
        self.assertEqual(
            b"/editor/submission/1/catalog/identifiers/1/?delete=true" in content,
            True)
        identifier = core_models.Identifier.objects.get(pk=1)
        self.assertEqual(int(identifier.value), 1)
        resp = self.client.get(reverse('identifiers_with_id',
                                       kwargs={'submission_id': self.book.id,
                                               'identifier_id': 1}))
        content = resp.content
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b"403" in content, False)
        resp = self.client.post(reverse('identifiers_with_id',
                                        kwargs={'submission_id': self.book.id,
                                                'identifier_id': 1}),
                                {'identifier': 'doi', 'digital_format': '',
                                 'update': '', 'physical_format': '',
                                 'value': 5, 'displayed': True})
        identifier = core_models.Identifier.objects.get(pk=1)
        self.assertEqual(int(identifier.value), 5)
        resp = self.client.get(reverse('update_contributor',
                                       kwargs={'submission_id': self.book.id,
                                               'contributor_type': 'author',
                                               'contributor_id': 1}))
        content = resp.content
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b"403" in content, False)
        self.assertEqual(b"rua_author_first_name" in content, True)
        resp = self.client.post(reverse('update_contributor',
                                        kwargs={'submission_id': self.book.id,
                                                'contributor_type': 'author',
                                                'contributor_id': 1}),
                                {'salutation': 'Mr',
                                 'first_name': 'rua_first_name',
                                 'last_name': 'rua_last_name',
                                 'middle_name': '', 'biography': 'updated bio',
                                 'institution': 'rua_testing', 'department': '',
                                 'country': 'GB', 'orcid': '', 'twitter': '',
                                 'facebook': '', 'linkedin': '',
                                 'author_email': 'fake_changed@fakeaddress.com'})
        found = False
        try:
            author = core_models.Author.objects.get(
                author_email='fake_changed@fakeaddress.com')
            found = True
        except:
            found = False
        self.assertEqual(found, True)
        resp = self.client.post(
            reverse('add_contributor',
                    kwargs={'submission_id': self.book.id,
                            'contributor_type': 'author'}),
            {'salutation': 'Mr',
             'first_name': 'rua_first_new_name',
             'last_name': 'rua_last_new_name',
             'middle_name': '',
             'biography': 'updated bio',
             'institution': 'rua_testing',
             'department': '',
             'country': 'GB',
             'orcid': '', 'twitter': '',
             'facebook': '', 'linkedin': '',
             'author_email': 'fake_changed@fakeaddress.com'}
        )

        self.assertEqual(resp.status_code, 302)
        found = True
        try:
            # Get new author without relying on hard coded pk
            author = core_models.Author.objects.get(
                first_name='rua_first_new_name'
            )
        except:
            found = False
        self.assertEqual(found, True)
        self.assertEqual(author.first_name, 'rua_first_new_name')
        self.assertEqual(author.last_name, 'rua_last_new_name')
        resp = self.client.post(
            reverse('delete_contributor',
            kwargs={'submission_id': self.book.id,
                    'contributor_type': 'author',
                    'contributor_id': author.pk})
        )
        found = True
        try:
            author = core_models.Author.objects.get(name='rua_first_new_name')
        except:
            found = False
        self.assertEqual(found, False)
        resp = self.client.get(
            reverse('retailers',
                    kwargs={'submission_id': self.book.id})
        )
        content = resp.content
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b"403" in content, False)
        self.assertEqual(b"Name" in content, True)
        self.assertEqual(b"Link" in content, True)
        self.assertEqual(b"Price" in content, True)
        self.assertEqual(b"Enabled" in content, True)
        self.assertEqual(b"Use the form to add a new retailer." in content, True)
        resp = self.client.post(
            reverse('retailers',
                    kwargs={'submission_id': self.book.id}),
            {'name': 'Amazon',
             'link': 'http://www.amazon.co.uk/mybook/',
             'price': '9.99',
             'enabled': True}
        )
        retailers = core_models.Retailer.objects.all()
        self.assertEqual(len(retailers), 1)
        resp_get = self.client.get(
            reverse('retailers',
                    kwargs={'submission_id': self.book.id})
        )
        content = resp_get.content
        self.assertEqual(resp_get.status_code, 200)
        self.assertEqual(b"403" in content, False)
        self.assertEqual(
            b"Use the form to add a new retailer." in content,
             False
        )
        self.assertEqual(
            b"/editor/submission/1/catalog/retailers/1/" in content,
            True
        )
        self.assertEqual(
            b"/editor/submission/1/catalog/retailers/1/?delete=true" in content,
            True)
        retailer = core_models.Retailer.objects.get(pk=1)
        self.assertEqual(int(retailer.price), int(9.99))
        resp = self.client.get(
            reverse('retailer_with_id',
                    kwargs={'submission_id': self.book.id,
                            'retailer_id': 1})
        )
        content = resp.content
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b"403" in content, False)
        resp = self.client.post(
            reverse('retailer_with_id',
                    kwargs={'submission_id': self.book.id,
                            'retailer_id': 1}),
            {'name': 'Amazon',
             'link': 'http://www.amazon.co.uk/mybook/',
             'price': '19.99', 'enabled': True,
             'update': ''}
        )
        retailer = core_models.Retailer.objects.get(pk=1)
        self.assertEqual(int(retailer.price), int(19.99))

        '''
		self.client.post(reverse('catalog',kwargs={'submission_id':self.book.id}),
			{'prefix':'prefix',
			'title':'title',
			'subtitle':'subtitle',
			'series':None,
			'description':'description',
			'license':'2',
			'pages':'15',
			'slug':'slug',
			'review_type':'open-with',
			'languages':'124',
			'publication_date':None}) 
			'''

    def test_view_chapter(self):
        resp = self.client.get(reverse('editor_view_chapter', kwargs={
            'submission_id': self.book.id,
            'chapter_id': self.chapter.id,
        }))
        content = resp.content
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b"Chapter Authors" in content, True)

    def test_handle_copyeditor_assignment(self):
        #  clear data
        assignments = core_models.CopyeditAssignment.objects.all()
        for assignment in assignments:
            assignment.delete()

        exception = None
        exception_raised = False
        try:
            logic.handle_copyeditor_assignment(
                request=self.factory.get('/'),
                book=self.book,
                copyedit=self.editor_user,
                files=[],
                due_date=datetime.date.today() + datetime.timedelta(days=9),
                note='This is a copyeditor assignment.',
                email_text='Dear...',
                requestor=self.superuser,
            )
        except BaseException as e:
            exception_raised = True
            exception = e

        self.assertFalse(exception_raised, msg=exception)

        assignments = core_models.CopyeditAssignment.objects.all()
        self.assertEqual(len(assignments), 1)

        # Cleanup
        for assignment in assignments:
            assignment.delete()

    def test_handle_duplicate_copyeditor_assignment(self):
        #  clear data
        assignments = core_models.CopyeditAssignment.objects.all()
        for assignment in assignments:
            assignment.delete()

        exception = None
        exception_raised = False
        try:
            for i in range(2):
                logic.handle_copyeditor_assignment(
                    request=self.factory.get('/'),
                    book=self.book,
                    copyedit=self.editor_user,
                    files=[],
                    due_date=datetime.date.today() + datetime.timedelta(days=9),
                    note='This is copyeditor assignment {num}.'.format(num=i),
                    email_text='Dear...',
                    requestor=self.superuser,
                )
        except BaseException as e:
            exception_raised = True
            exception = e

        self.assertFalse(exception_raised, msg=exception)

        assignments = core_models.CopyeditAssignment.objects.all()
        self.assertEqual(len(assignments), 2)

        # Cleanup
        for assignment in assignments:
            assignment.delete()

    def test_handle_indexer_assignment(self):
        #  clear data
        assignments = core_models.IndexAssignment.objects.all()
        for assignment in assignments:
            assignment.delete()

        exception = None
        exception_raised = False
        try:
            logic.handle_indexer_assignment(
                request=self.factory.get('/'),
                book=self.book,
                index=self.editor_user,
                files=[],
                due_date=datetime.date.today() + datetime.timedelta(days=9),
                note='This is a indexer assignment.',
                email_text='Dear...',
                requestor=self.superuser,
                attachment=None,
            )
        except BaseException as e:
            exception_raised = True
            exception = e

        self.assertFalse(exception_raised, msg=exception)

        assignments = core_models.IndexAssignment.objects.all()
        self.assertEqual(len(assignments), 1)

        # Cleanup
        for assignment in assignments:
            assignment.delete()

    def test_handle_duplicate_indexer_assignment(self):
        #  clear data
        assignments = core_models.IndexAssignment.objects.all()
        for assignment in assignments:
            assignment.delete()

        exception = None
        exception_raised = False
        try:
            for i in range(2):
                logic.handle_indexer_assignment(
                    request=self.factory.get('/'),
                    book=self.book,
                    index=self.editor_user,
                    files=[],
                    due_date=datetime.date.today() + datetime.timedelta(days=9),
                    note='This is indexer assignment {num}.'.format(num=i),
                    email_text='Dear...',
                    requestor=self.superuser,
                    attachment=None,
                )
        except BaseException as e:
            exception_raised = True
            exception = e

        self.assertFalse(exception_raised, msg=exception)

        assignments = core_models.IndexAssignment.objects.all()
        self.assertEqual(len(assignments), 2)

        # Cleanup
        for assignment in assignments:
            assignment.delete()

    def test_handle_typeset_assignment(self):
        #  clear data
        assignments = core_models.TypesetAssignment.objects.all()
        for assignment in assignments:
            assignment.delete()

        exception = None
        exception_raised = False
        try:
            logic.handle_typeset_assignment(
                request=self.factory.get('/'),
                book=self.book,
                typesetter=self.editor_user,
                files=[],
                due_date=datetime.date.today() + datetime.timedelta(days=9),
                email_text='Dear...',
                requestor=self.superuser,
                attachment=None,
            )
        except BaseException as e:
            exception_raised = True
            exception = e

        self.assertFalse(exception_raised, msg=exception)

        assignments = core_models.TypesetAssignment.objects.all()
        self.assertEqual(len(assignments), 1)

        # Cleanup
        for assignment in assignments:
            assignment.delete()

    def test_handle_duplicate_typeset_assignment(self):
        #  clear data
        assignments = core_models.TypesetAssignment.objects.all()
        for assignment in assignments:
            assignment.delete()

        exception = None
        exception_raised = False
        try:
            for i in range(2):
                logic.handle_typeset_assignment(
                    request=self.factory.get('/'),
                    book=self.book,
                    typesetter=self.editor_user,
                    files=[],
                    due_date=datetime.date.today() + datetime.timedelta(days=9),
                    email_text='Dear...',
                    requestor=self.superuser,
                    attachment=None,
                )
        except BaseException as e:
            exception_raised = True
            exception = e

        self.assertFalse(exception_raised, msg=exception)

        assignments = core_models.TypesetAssignment.objects.all()
        self.assertEqual(len(assignments), 2)

        # Cleanup
        for assignment in assignments:
            assignment.delete()
