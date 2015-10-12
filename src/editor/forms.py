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

	file = forms.FileField(required=False)
	identifier = forms.CharField(required=True)
	name = forms.CharField(required=True)

class UploadContract(forms.ModelForm):

	class Meta:
		model = core_models.Contract
		exclude = ('author_file',)

class AuthorContractSignoff(forms.ModelForm):

	class Meta:
		model = core_models.Contract
		fields = ('author_file',)



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

class Typeset(forms.ModelForm):

	class Meta:
		model = core_models.TypesetAssignment
		fields = ('note',)

class TypesetAuthorInvite(forms.ModelForm):

	class Meta:
		model = core_models.TypesetAssignment
		fields = ('note_to_author',)

class TypesetAuthor(forms.ModelForm):

	class Meta:
		model = core_models.TypesetAssignment
		fields = ('note_from_author',)

class TypesetTypesetterInvite(forms.ModelForm):

	class Meta:
		model = core_models.TypesetAssignment
		fields = ('note_to_typesetter',)


class TypesetTypesetter(forms.ModelForm):

	class Meta:
		model = core_models.TypesetAssignment
		fields = ('note_from_typesetter',)
