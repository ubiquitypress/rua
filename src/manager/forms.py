from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

from manager import models
from core import models as core_models
from review import models as review_models
from pprint import pprint

class GroupForm(forms.ModelForm):

	class Meta:
		model = models.Group
		exclude = ()
class FormElementForm(forms.ModelForm):

	class Meta:
		model = review_models.FormElement
		exclude = ()
class FormElementsRelationshipForm(forms.ModelForm):

	class Meta:
		model = review_models.FormElementsRelationship
		exclude = ()

class StagesProposalForm(forms.ModelForm):

	class Meta:
		model = core_models.ProposalForm
		exclude = ()
	def __init__(self, *args, **kwargs):
		super(StagesProposalForm, self).__init__(*args, **kwargs)
		self.fields['intro_text'].label = "Introduction text"

class StagesProposalFormElementForm(forms.ModelForm):

	class Meta:
		model = core_models.ProposalFormElement
		exclude = ()
class StagesProposalFormElementRelationshipForm(forms.ModelForm):

	class Meta:
		model = core_models.ProposalFormElementsRelationship
		exclude = ()
class ReviewForm(forms.ModelForm):

	class Meta:
		model = review_models.Form
		exclude = ()
	def __init__(self, *args, **kwargs):
		super(ReviewForm, self).__init__(*args, **kwargs)
		self.fields['intro_text'].label = "Introduction text"
		
class EditKey(forms.Form):

	def __init__(self, *args, **kwargs):
		key_type = kwargs.pop('key_type', None)
		value = kwargs.pop('value', None)
		super(EditKey, self).__init__(*args, **kwargs)

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

class ProposalForm(forms.Form):

	def __init__(self, *args, **kwargs):
		super(ProposalForm, self).__init__(*args, **kwargs)
		self.fields['selection'].choices = [(proposal_form.pk, proposal_form) for proposal_form in core_models.ProposalForm.objects.all()]

	selection = forms.ChoiceField(widget=forms.Select)

class DefaultReviewForm(forms.Form):

	name = forms.CharField(widget=forms.TextInput, required=True)
	ref = forms.CharField(widget=forms.TextInput, required=True)
	intro_text = forms.CharField(widget=forms.Textarea, required=True)
	completion_text = forms.CharField(widget=forms.Textarea, required=True)

class DefaultForm(forms.Form):

	title = forms.CharField(widget=forms.TextInput, required=True)
	subtitle = forms.CharField(widget=forms.TextInput, required=False)
	author = forms.CharField(widget=forms.TextInput, required=True)

	def clean(self):
		cleaned_data = self.cleaned_data

def render_choices(choices):
	c_split = choices.split('|')
	return [(choice.capitalize(), choice) for choice in c_split]

class GeneratedForm(forms.Form):

	def __init__(self, *args, **kwargs):

		form_obj = kwargs.pop('form', None)
		super(GeneratedForm, self).__init__(*args, **kwargs)
		relations = core_models.ProposalFormElementsRelationship.objects.filter(form__id=form_obj.id).order_by('order')
		for relation in relations:

			if relation.element.field_type == 'text':
				self.fields[relation.element.name] = forms.CharField(widget=forms.TextInput(attrs={'div_class':relation.width}), required=relation.element.required)
			elif relation.element.field_type == 'textarea':
				self.fields[relation.element.name] = forms.CharField(widget=forms.Textarea(attrs={'div_class':relation.width}), required=relation.element.required)
			elif relation.element.field_type == 'date':
				self.fields[relation.element.name] = forms.CharField(widget=forms.DateInput(attrs={'class':'datepicker', 'div_class':relation.width}), required=relation.element.required)
			elif relation.element.field_type == 'upload':
				self.fields[relation.element.name] = forms.FileField(widget=forms.FileInput(attrs={'div_class':relation.width}), required=relation.element.required)
			elif relation.element.field_type == 'select':
				if relation.element.name == 'Series':
					choices = series_list
				else:
					choices = render_choices(relation.element.choices)
				self.fields[relation.element.name] = forms.ChoiceField(widget=forms.Select(attrs={'div_class':relation.width}), choices=choices, required=relation.element.required)
			elif relation.element.field_type == 'email':
				self.fields[relation.element.name] = forms.EmailField(widget=forms.TextInput(attrs={'div_class':relation.width}), required=relation.element.required)
			elif relation.element.field_type == 'check':
				self.fields[relation.element.name] = forms.BooleanField(widget=forms.CheckboxInput(attrs={'is_checkbox':True, 'div_class':relation.width}), required=relation.element.required)
			self.fields[relation.element.name].help_text = relation.help_text


class GeneratedReviewForm(forms.Form):

	def __init__(self, *args, **kwargs):

		form_obj = kwargs.pop('form', None)
		super(GeneratedReviewForm, self).__init__(*args, **kwargs)
		relations = review_models.FormElementsRelationship.objects.filter(form=form_obj).order_by('order')
		for relation in relations:

			if relation.element.field_type == 'text':
				self.fields[relation.element.name] = forms.CharField(widget=forms.TextInput(attrs={'div_class':relation.width}), required=relation.element.required)
			elif relation.element.field_type == 'textarea':
				self.fields[relation.element.name] = forms.CharField(widget=forms.Textarea(attrs={'div_class':relation.width}), required=relation.element.required)
			elif relation.element.field_type == 'date':
				self.fields[relation.element.name] = forms.CharField(widget=forms.DateInput(attrs={'class':'datepicker', 'div_class':relation.width}), required=relation.element.required)
			elif relation.element.field_type == 'upload':
				self.fields[relation.element.name] = forms.FileField(widget=forms.FileInput(attrs={'div_class':relation.width}), required=relation.element.required)
			elif relation.element.field_type == 'select':
				if relation.element.name == 'Series':
					choices = series_list
				else:
					choices = render_choices(relation.element.choices)
				self.fields[relation.element.name] = forms.ChoiceField(widget=forms.Select(attrs={'div_class':relation.width}), choices=choices, required=relation.element.required)
			elif relation.element.field_type == 'email':
				self.fields[relation.element.name] = forms.EmailField(widget=forms.TextInput(attrs={'div_class':relation.width}), required=relation.element.required)
			elif relation.element.field_type == 'check':
				self.fields[relation.element.name] = forms.BooleanField(widget=forms.CheckboxInput(attrs={'is_checkbox':True, 'div_class':relation.width}), required=relation.element.required)
			self.fields[relation.element.name].help_text = relation.help_text

