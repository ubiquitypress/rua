from django import forms
from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives

from core import models as core_models
from submission import models
from core import logic

class SubmitProposal(forms.ModelForm):

	class Meta:
		model = models.Proposal
		fields = ('title', 'subtitle', 'description', 'notes', 'uploaded_file', 'funding')


class SubmitBookStageOne(forms.ModelForm):

	class Meta:
		model = core_models.Book
		fields = ('book_type', 'cover_letter', 'series', 'license')

class SubmitBookStageTwo(forms.ModelForm):

	class Meta:
		model = core_models.Book
		fields = ('prefix', 'title', 'subtitle', 'description')

class SubmitBook(forms.ModelForm):

	class Meta:
		model = core_models.Book
		fields = ('title', 'subtitle', 'description', 'subject', 'license', 'cover_letter', 'series')

class AuthorForm(forms.ModelForm):

	class Meta:
		model = core_models.Author
		exclude = ()

class EditorForm(forms.ModelForm):

	class Meta:
		model = core_models.Editor
		exclude = ()
