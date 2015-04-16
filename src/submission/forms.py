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

class SubmitBook(forms.ModelForm):
	
	class Meta:
		model = core_models.Book
		fields = ('title', 'subtitle', 'description', 'subject')
