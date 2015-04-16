from django import forms
from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from core import models
from core import logic

import uuid

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

		