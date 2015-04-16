from django import forms
from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple

class SubmitAgreements(ModelForm):
	publication_fees = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={'id':'publication_fees'}))
	submission_requirements = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={'id':'submission_requirements'}))
	copyright_notice = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={'id':'copyright_notice'}))
	comments_editor = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder': 'any additional information an editor may require to make a decision', 'style': 'width: 100%; height: 100px'}))

	class Meta:
		model = models.Article
		