from django import forms
from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from functools import partial

from core import models
from core import logic

import uuid

class UploadMiscFile(forms.Form):

	label = forms.CharField(required=True)
	file_type = forms.ChoiceField(required=True, choices=(('marketing', 'Marketing'), ('agreements', 'Agreements'), ('other', 'Other')))

class UploadFile(forms.Form):

	label = forms.CharField(required=True)

class UserCreationForm(forms.ModelForm):
	"""
	A form that creates a user, with no privileges, from the given username and
	password.
	"""
	error_messages = {
		'password_mismatch': ("The two password fields didn't match."),
	}
	password1 = forms.CharField(label=("Password"),
		widget=forms.PasswordInput)
	password2 = forms.CharField(label=("Password confirmation"),
		widget=forms.PasswordInput,
		help_text=("Enter the same password as above, for verification."))

	class Meta:
		model = User
		fields = ("username", "first_name", "last_name", "email")

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError(
				self.error_messages['password_mismatch'],
				code='password_mismatch',
			)
		return password2

	def save(self, commit=True):
		user = super(UserCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		user.is_active = False
		user.save()

		# Add a profile for this new user and create a new activation code.
		profile = models.Profile(user=user, activation_code=uuid.uuid4())
		profile.terms_and_conditions = True;
		profile.save()

		# Send email to the user 
		subject, from_email, to = 'Registration Confirmation', "from_address@press.com", user.email
		html_template = 'email/html_register.html'
		text_template = 'email/text_register.html'
		context = {'user': user, 'profile': profile, 'base_url': settings.BASE_URL}
		logic.send_email(subject=subject, context=context, from_email=from_email, to=to, html_template=html_template, text_template=text_template)
		

		if commit:
			user.save()
		return user

class UserProfileForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ("first_name", "last_name", "email")

class FullUserProfileForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ("username", "first_name", "last_name", "email")

class ProfileForm(forms.ModelForm):

	class Meta:
		model = models.Profile
		fields = ("salutation", "middle_name", "biography","interest", "orcid", "institution", "department", "country", "twitter", "facebook", "linkedin", "impactstory", "github", "profile_image", "signature","website")

class FullProfileForm(forms.ModelForm):

	class Meta:
		model = models.Profile
		fields = ("salutation", "middle_name", "biography", "orcid", "institution", "department","interest", "country", "twitter", "facebook", "linkedin", "impactstory", "github", "profile_image", "signature","website", "roles")

class TaskForm(forms.ModelForm):

	class Meta:
		model = models.Task
		fields = ("text","workflow")
		exclude = ("due",)

class RecommendationForm(forms.ModelForm):

	class Meta:
		model = models.ReviewAssignment
		fields = ("recommendation", "competing_interests")

	def __init__(self, *args, **kwargs):
		ci_required = kwargs.pop('ci_required', None)
		super(RecommendationForm, self).__init__(*args, **kwargs)

		if ci_required == 'on':
			self.fields['competing_interests'] = forms.CharField(widget=forms.Textarea, required=True)

class MessageForm(forms.ModelForm):

	class Meta:
		model = models.Message
		fields = ('message', )

class Copyedit(forms.ModelForm):

	class Meta:
		model = models.CopyeditAssignment
		fields = ('note',)

class CopyeditAuthorInvite(forms.ModelForm):

	class Meta:
		model = models.CopyeditAssignment
		fields = ('note_to_author',)

class CopyeditAuthor(forms.ModelForm):

	class Meta:
		model = models.CopyeditAssignment
		fields = ('note_from_author',)


class Typeset(forms.ModelForm):

	class Meta:
		model = models.TypesetAssignment
		fields = ('note',)


class TypesetAuthorInvite(forms.ModelForm):

	class Meta:
		model = models.TypesetAssignment
		fields = ('note_to_author',)

class TypesetAuthor(forms.ModelForm):

	class Meta:
		model = models.TypesetAssignment
		fields = ('note_from_author',)

class TypesetTypesetterInvite(forms.ModelForm):

	class Meta:
		model = models.TypesetAssignment
		fields = ('note_to_typesetter',)


class TypesetTypesetter(forms.ModelForm):

	class Meta:
		model = models.TypesetAssignment
		fields = ('note_from_typesetter',)

#####WORKFLOW forms #####

class FormatForm(forms.ModelForm):

	format_file = forms.FileField(required=True)

	class Meta:
		model = models.Format
		exclude = ('book', 'file')
		
class FormatFormInitial(forms.ModelForm):

	class Meta:
		model = models.Format
		exclude = ('book', 'file')

class ChapterForm(forms.ModelForm):

	chapter_file = forms.FileField(required=True)

	class Meta:
		model = models.Chapter
		exclude = ('book', 'file')

class ChapterFormInitial(forms.ModelForm):

	class Meta:
		model = models.Chapter
		exclude = ('book', 'file')

class UpdateChapterFormat(forms.Form):

	file = forms.FileField(required=True)
	file_label = forms.CharField(required=False)
	name = forms.CharField(required=True)

class UploadContract(forms.ModelForm):

	class Meta:
		model = models.Contract
		exclude = ('author_file',)

class AuthorContractSignoff(forms.ModelForm):

	class Meta:
		model = models.Contract
		fields = ('author_file',)

class EditMetadata(forms.ModelForm):

	class Meta:
		model = models.Book
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
		model = models.Identifier
		fields = ('identifier', 'value', 'displayed')

class CoverForm(forms.ModelForm):

	class Meta:
		model = models.Book
		fields = ('cover',)

class RetailerForm(forms.ModelForm):

	class Meta:
		model = models.Retailer
		fields = ('name', 'link', 'price', 'enabled')

		
