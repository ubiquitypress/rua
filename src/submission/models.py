from django.db import models
from django.contrib.auth.models import User

def proposal_status():
	return (
		('submission', 'Submission'),
		('revisions_required', 'Revisions Required'),
		('revisions_submitted', 'Revisions Submitted'),
		('accepted', 'Accepted'),
		('declined', 'Declined'),
	)

def book_type_choices():
	return (
		('monograph', 'Monograph'),
		('edited_volume', 'Edited Volume'),
	)

class Proposal(models.Model):


	owner = models.ForeignKey(User,blank=True, null=True)
	title = models.CharField(max_length=255, verbose_name='Book Title')
	subtitle = models.CharField(max_length=255)
	author = models.CharField(max_length=255, verbose_name='Submitting author/editor')
	date_submitted = models.DateTimeField(auto_now_add=True)
	form = models.ForeignKey('core.ProposalForm')
	data = models.TextField(blank=True, null=True)
	date_review_started = models.DateTimeField(blank=True, null=True)
	review_assignments = models.ManyToManyField('ProposalReview', related_name='review', null=True, blank=True)
	review_form = models.ForeignKey('review.Form', null=True, blank=True)
	requestor = models.ForeignKey(User, null=True,blank=True,related_name="editor_requestor")
	revision_due_date = models.DateTimeField(blank=True, null=True)
	date_accepted = models.DateTimeField(blank=True, null=True)
	book_type = models.CharField(max_length=50, null=True, blank=True, choices=book_type_choices(), help_text="A monograph is a work authored, in its entirety, by one or more authors. An edited volume has different authors for each chapter.")
	
	status = models.CharField(max_length=20, choices=proposal_status(), default='submission')

	def status_verbose(self):
		return dict(proposal_status())[self.status]


class SubmissionChecklistItem(models.Model):

	slug = models.CharField(max_length=100)
	text = models.CharField(max_length=500)
	sequence = models.IntegerField(default=999)
	required = models.BooleanField(default=True)

	class Meta:
		ordering = ('sequence', 'text')

def review_recommendation():
	return (
		('accept', 'Accept'),
		('reject', 'Reject'),
		('revisions', 'Revisions Required')
	)

class ProposalReview(models.Model):
	proposal = models.ForeignKey(Proposal) #TODO: Remove this as it is already linked to the book through the review round
	user = models.ForeignKey(User)
	assigned = models.DateField(auto_now=True)
	accepted = models.DateField(blank=True, null=True)
	declined = models.DateField(blank=True, null=True)
	due = models.DateField(blank=True, null=True)
	completed = models.DateField(blank=True, null=True)
	files = models.ManyToManyField('core.File', blank=True, null=True)
	results = models.ForeignKey('review.FormResult', null=True, blank=True)
	recommendation = models.CharField(max_length=10, choices=review_recommendation(), null=True, blank=True)
	competing_interests = models.TextField(blank=True, null=True, help_text="If any of the authors or editors have any competing interests please add them here. EG. 'This study was paid for by corp xyz.'")
	blind = models.NullBooleanField(default=False, blank=True, null=True)

	#Reopened
	comments_from_editor = models.TextField(blank=True, null=True, help_text="If any editors have any comments for the reviewer")
	reopened = models.BooleanField(default=False)
	withdrawn = models.BooleanField(default=False)

	class Meta:
		unique_together = ('proposal', 'user')

	def __unicode__(self):
		return u'%s - %s %s' % (self.pk, self.proposal.title, self.user.username)

	def __repr__(self):
		return u'%s - %s %s' %  (self.pk, self.proposal.title, self.user.username)
