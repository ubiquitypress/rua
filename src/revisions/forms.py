from django import forms
from django.forms import ModelForm
from revisions import models

class AuthorRevisionForm(ModelForm):

	class Meta:
		model = models.Revision
		fields = ('cover_letter',)