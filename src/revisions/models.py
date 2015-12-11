from django.db import models
from django.contrib.auth.models import User

def revision_choices():
	return (
		('submission', 'Submission'),
		('review', 'Review'),
	)

class Revision(models.Model):
	book = models.ForeignKey('core.Book')
	notes_from_editor = models.TextField(help_text='Enter some information to assist the author/editors with their revisions. It is best that you use full sentences in your notes.')
	cover_letter = models.TextField(blank=True, null=True)
	revision_type = models.CharField(max_length=100, choices=revision_choices())
	requestor = models.ForeignKey(User)

	requested = models.DateField(auto_now_add=True)
	due = models.DateField(blank=True, null=True, help_text='Set the date the revisions are due. The author will be reminded once before the due date and once after.')
	completed = models.DateField(blank=True, null=True)

	overdue_reminder = models.BooleanField(default=False)
