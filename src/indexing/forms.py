from django import forms
from django.forms import ModelForm
from core import models

class Index(forms.ModelForm):

	class Meta:
		model = models.IndexAssignment
		fields = ('note_from_indexer',)
