from django.db import models

# Create your models here.
class Proposal(models.Model):

	title = models.CharField(max_length=255)
	description = models.TextField(blank=True, null=True)
	notes = models.TextField(blank=True, null=True)
	uploaded_file = models.FileField()
