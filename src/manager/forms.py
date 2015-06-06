from django import forms
from django.forms import ModelForm

from manager import models

class GroupForm(forms.ModelForm):

    class Meta:
        model = models.Group
        exclude = ()
