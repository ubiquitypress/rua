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

class UpdateChapterFormat(forms.Form):

	file = forms.FileField(required=True)
	name = forms.CharField(required=True)

class UploadContract(forms.ModelForm):

	class Meta:
		model = core_models.Contract
		exclude = ('author_file',)

class AuthorContractSignoff(forms.ModelForm):

	class Meta:
		model = core_models.Contract
		fields = ('author_file',)
