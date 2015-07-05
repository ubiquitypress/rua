from django import forms
from django.forms import ModelForm
from core import models as core_models

class FormatForm(forms.ModelForm):

	format_file = forms.FileField(required=True)

	class Meta:
		model = core_models.Format
		exclude = ('book', 'file')

class ChapterForm(forms.ModelForm):

	chapter_file = forms.FileField(required=True)

	class Meta:
		model = core_models.Chapter
		exclude = ('book', 'file')
