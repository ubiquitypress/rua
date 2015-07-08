from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Proposal(models.Model):

	title = models.CharField(max_length=255)
	subtitle = models.CharField(max_length=255,blank=True, null=True)
	funding = models.TextField(max_length=500, blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	notes = models.TextField(blank=True, null=True)
	uploaded_file = models.FileField()
	owner = models.ForeignKey(User)

class SubmissionChecklistItem(models.Model):
	slug = models.CharField(max_length=100)
	text = models.CharField(max_length=500)
	sequence = models.IntegerField(default=999)
	required = models.BooleanField(default=True)

	class Meta:
		ordering = ('sequence', 'text')
