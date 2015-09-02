from django import forms
from django.forms import ModelForm
from core import models

class Typeset(forms.ModelForm):

	class Meta:
		model = models.CopyeditAssignment
		fields = ('note',)


class TypesetAuthorInvite(forms.ModelForm):

	class Meta:
		model = models.CopyeditAssignment
		fields = ('note_to_author',)

class TypesetAuthor(forms.ModelForm):

	class Meta:
		model = models.CopyeditAssignment
		fields = ('note_from_author',)