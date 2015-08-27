from django import forms
from django.forms import ModelForm
from revisions import models

class RevisionForm(ModelForm):

	class Meta:
		model = models.Revision
		fields = ('notes_from_editor', 'due')

class AuthorRevisionForm(ModelForm):

	class Meta:
		model = models.Revision
		fields = ('cover_letter',)