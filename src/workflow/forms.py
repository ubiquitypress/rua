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

class UploadMiscFile(forms.Form):

	label = forms.CharField(required=True)
	file_type = forms.ChoiceField(required=True, choices=(('marketing', 'Marketing'), ('agreements', 'Agreements'), ('other', 'Other')))

class EditMetadata(forms.ModelForm):

	class Meta:
		model = core_models.Book
		fields = (
			'prefix',
			'title',
			'subtitle',
			'series',
			'description',
			'license',
			'pages',
			'slug',
			'review_type',
			'languages',
			'publication_date'
		)

		widgets = {
            'languages': forms.CheckboxSelectMultiple(),
        }

class IdentifierForm(forms.ModelForm):

	class Meta:
		model = core_models.Identifier
		fields = ('identifier', 'value', 'displayed')

class CoverForm(forms.ModelForm):

	class Meta:
		model = core_models.Book
		fields = ('cover',)

class RetailerForm(forms.ModelForm):

	class Meta:
		model = core_models.Retailer
		fields = ('name', 'link', 'price', 'enabled')
