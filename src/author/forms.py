from django import forms
from django.forms import ModelForm
from core import models as core_models

class UploadContract(forms.ModelForm):

	class Meta:
		model = core_models.Contract
		exclude = ('author_file',)

class AuthorContractSignoff(forms.ModelForm):

	class Meta:
		model = core_models.Contract
		fields = ('author_file',)