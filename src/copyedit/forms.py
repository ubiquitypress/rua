from django import forms
from django.forms import ModelForm
from core import models

class Copyedit(forms.ModelForm):

	class Meta:
		model = models.CopyeditAssignment
		fields = ('note',)

class CopyeditAuthorInvite(forms.ModelForm):

	class Meta:
		model = models.CopyeditAssignment
		fields = ('note_to_author',)

class CopyeditAuthor(forms.ModelForm):

	class Meta:
		model = models.CopyeditAssignment
		fields = ('note_from_author',)