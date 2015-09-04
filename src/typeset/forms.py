from django import forms
from django.forms import ModelForm
from core import models

class Typeset(forms.ModelForm):

	class Meta:
		model = models.TypesetAssignment
		fields = ('note',)


class TypesetAuthorInvite(forms.ModelForm):

	class Meta:
		model = models.TypesetAssignment
		fields = ('note_to_author',)

class TypesetAuthor(forms.ModelForm):

	class Meta:
		model = models.TypesetAssignment
		fields = ('note_from_author',)

class TypesetTypesetterInvite(forms.ModelForm):

	class Meta:
		model = models.TypesetAssignment
		fields = ('note_to_typesetter',)