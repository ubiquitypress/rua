from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

from manager import models

class GroupForm(forms.ModelForm):

    class Meta:
        model = models.Group
        exclude = ()

class EditKey(forms.Form):

	def __init__(self, *args, **kwargs):
		key_type = kwargs.pop('key_type', None)
		value = kwargs.pop('value', None)
		super(EditKey, self).__init__(*args, **kwargs)

		print key_type, value
		if key_type == 'rich_text':
			self.fields['value'].widget = SummernoteWidget()
		elif key_type == 'boolean':
			self.fields['value'].widget = forms.CheckboxInput()
		elif key_type == 'integer':
			self.fields['value'].widget = forms.TextInput(attrs={'type': 'number'})
		elif key_type == 'file' or key_type == 'journalthumb':
			self.fields['value'].widget = forms.FileInput()
		elif key_type == 'text':
			self.fields['value'].widget = forms.Textarea()
		else:
			self.fields['value'].widget.attrs['size'] = '100%'

		self.fields['value'].initial = value

	value = forms.CharField(label='')

	def clean(self):
		cleaned_data = self.cleaned_data
