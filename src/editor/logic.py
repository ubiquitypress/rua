from django.db.models import Q
from django.db.models import Max

from django.db.models import Max
from django.utils import timezone
from django.contrib import messages
from core import models, email, log
from submission import logic as submission_logic

import json


def generate_digital_choices(digital_formats):
	return [('', '------')] + [(frmt.id, "%s - %s" % (frmt.name,  frmt.get_file_type_display())) for frmt in digital_formats]

def generate_physical_choices(physical_formats):
	return [('', '------')] + [(frmt.id, "%s - %s" % (frmt.name,  frmt.get_file_type_display())) for frmt in physical_formats]

def send_author_invite(submission, copyedit, email_text, sender, attachment=None):
	from_email = models.Setting.objects.get(group__name='email', name='from_address')

	context = {
		'base_url': models.Setting.objects.get(group__name='general', name='base_url').value,
		'submission': submission,
		'copyedit': copyedit,
		'sender': sender,
	}

	email.send_email('Copyediting Completed', context, from_email.value, submission.owner.email, email_text, book=submission, attachment=attachment)


def handle_copyeditor_assignment(request,book, copyedit, files, due_date, note, email_text, requestor, attachment=None):
	try:   
		new_copyeditor = models.CopyeditAssignment(
			book = book,
			copyeditor = copyedit,
			requestor = requestor,
			note=note,
			due = due_date,
		)

		new_copyeditor.save()

		for _file in files:
			new_copyeditor.files.add(_file)

		new_copyeditor.save()

		log.add_log_entry(book=book, user=requestor, kind='copyedit', message='Copyeditor %s %s assigned. Due %s' % (copyedit.first_name, copyedit.last_name, due_date), short_name='Copyedit Assignment')
		send_copyedit_assignment(book, new_copyeditor, email_text, requestor, attachment=attachment)
	except:
		messages.add_message(request, messages.WARNING, 'Copyedit Assignment for user <%s> already exists. User might already exist in one of the selected committees' % copyedit.username)
  


def handle_indexer_assignment(request,book, index, files, due_date, note, email_text, requestor, attachment):
	try:
		new_indexer = models.IndexAssignment(
			book=book,
			indexer=index,
			requestor=requestor,
			note=note,
			due=due_date,
		)

		new_indexer.save()

		for _file in files:
			new_indexer.files.add(_file)

		new_indexer.save()

		send_invite_indexer(book, new_indexer, email_text, requestor, attachment)

		log.add_log_entry(book=book, user=requestor, kind='index', message='Indexer %s %s assigned. Due %s' % (index.first_name, index.last_name, due_date), short_name='Indexing Assignment')
	except:
		   messages.add_message(request, messages.WARNING, 'Indexing Assignment for user <%s> already exists. User might already exist in one of the selected committees' % index.username)
  

def handle_typeset_assignment(request,book, typesetter, files, due_date, email_text, requestor, attachment):
	try:
		new_typesetter = models.TypesetAssignment(
			book=book,
			typesetter=typesetter,
			requestor=requestor,
			due=due_date,
			note=email_text,
		)

		new_typesetter.save()

		for _file in files:
			new_typesetter.files.add(_file)

		new_typesetter.save()

		send_invite_typesetter(book, new_typesetter, email_text, requestor, attachment)

		log.add_log_entry(book=book, user=requestor, kind='typeset', message='Typesetter %s %s assigned. Due %s' % (typesetter.first_name, typesetter.last_name, due_date), short_name='Typeset Assignment')
	except:
		   messages.add_message(request, messages.WARNING, 'Typeset Assignment for user <%s> already exists. User might already exist in one of the selected committees' % typesetter.username)
  



def send_copyedit_assignment(submission, copyedit, email_text, sender, attachment):
	from_email = models.Setting.objects.get(group__name='email', name='from_address')
	press_name = models.Setting.objects.get(group__name='general', name='press_name').value

	context = {
		'base_url': models.Setting.objects.get(group__name='general', name='base_url').value,
		'submission': submission,
		'copyedit': copyedit,
		'sender': sender,
		'press_name':press_name,
	}

	email.send_email('Copyedit Assignment', context, from_email.value, copyedit.copyeditor.email, email_text, book=submission, attachment=attachment)


def send_invite_indexer(book, index, email_text, sender, attachment):
	from_email = models.Setting.objects.get(group__name='email', name='from_address')

	context = {
		'base_url': models.Setting.objects.get(group__name='general', name='base_url').value,
		'submission': book,
		'index': index,
		'sender': sender,
	}

	email.send_email('Indexing Request', context, from_email.value, index.indexer.email, email_text, book=book, attachment=attachment)


def get_submission_tasks(book, user):
	task_list = []
	base_url = models.Setting.objects.get(group__name='general', name='base_url').value

	copyedit_tasks = models.CopyeditAssignment.objects.filter(book=book, completed__isnull=False, editor_review__isnull=True, author_completed__isnull=True)
	typeset_tasks = models.TypesetAssignment.objects.filter((Q(completed__isnull=False) & Q(editor_review__isnull=True)) | (Q(author_completed__isnull=False) & Q(editor_second_review__isnull=True)), book=book, requestor=user)

	for copyedit in copyedit_tasks:
		task_list.append({'type': 'copyedit', 'book': copyedit.book, 'task': 'Copyedit Review', 'date': copyedit.completed, 'title': copyedit.book.title, 'url': 'http://%s/editor/submission/%s/editing/view/copyeditor/%s/' % (base_url, copyedit.book.id, copyedit.id)})

	for typeset in typeset_tasks:
		task_list.append({'type': 'typeset', 'book': typeset.book, 'task': 'Typesetting Review', 'date': typeset.completed, 'title': typeset.book.title, 'url': 'http://%s/editor/submission/%s/production/view/typesetter/%s' % (base_url, typeset.book.id, typeset.id)})

	return task_list

def create_new_review_round(book):
	latest_round = models.ReviewRound.objects.filter(book=book).aggregate(max=Max('round_number'))
	next_round = latest_round.get('max')+1 if latest_round.get('max') > 0 else 1
	return models.ReviewRound.objects.create(book=book, round_number=next_round)

def handle_review_assignment(request,book, reviewer, review_type, due_date, review_round, user, email_text, attachment=None):
	obj, created = models.ReviewAssignment.objects.get_or_create(
			review_type=review_type,
			user=reviewer,
			book=book,
			review_round=review_round,defaults={'due':due_date}
	)

	if created:
		book.review_assignments.add(obj)
		log.add_log_entry(book=book, user=user, kind='review', message='Reviewer %s %s assigned. Round %d' % (reviewer.first_name, reviewer.last_name, review_round.round_number), short_name='Review Assignment')
		send_review_request(book, obj, email_text, user, attachment)
		return created
	else:
		messages.add_message(request, messages.WARNING, 'Review Assignment for user <%s> already exists. User might already exist in one of the selected committees' % reviewer.username)
		return obj


# Email Handlers - TODO: move to email.py?

def send_review_request(book, review_assignment, email_text, sender, attachment=None):
	from_email = models.Setting.objects.get(group__name='email', name='from_address')
	base_url = models.Setting.objects.get(group__name='general', name='base_url')
	press_name = models.Setting.objects.get(group__name='general', name='press_name').value

	decision_url = 'http://%s/review/%s/%s/assignment/%s/decision/' % (base_url.value, review_assignment.review_type, book.id, review_assignment.id)

	context = {
		'book': book,
		'review': review_assignment,
		'decision_url': decision_url,
		'sender': sender,
		'base_url':base_url.value,
		'press_name':press_name,
	}

	email.send_email('Review Request', context, from_email.value, review_assignment.user.email, email_text, book=book, attachment=attachment)

def send_review_update(book, review_assignment, email_text, sender, attachment=None):
	from_email = models.Setting.objects.get(group__name='email', name='from_address')
	base_url = models.Setting.objects.get(group__name='general', name='base_url')

	print email_text
	context = {
		'book': book,
		'review': review_assignment,
		'sender': sender,
	}

	email.send_email('Review Assignment %s: Due Date Updated' % review_assignment.id, context, from_email.value, review_assignment.user.email, email_text, book=book, attachment=attachment)

def send_proposal_decline(proposal, email_text, sender):
	from_email = models.Setting.objects.get(group__name='email', name='from_address')

	context = {
		'proposal': proposal,
		'sender': sender,
	}

	email.send_email('[abp] Proposal Declined', context, from_email.value, proposal.owner.email, email_text)

def send_proposal_accept(proposal, email_text, submission, sender, attachment=None):
	from_email = models.Setting.objects.get(group__name='email', name='from_address')

	context = {
		'base_url': models.Setting.objects.get(group__name='general', name='base_url').value,
		'proposal': proposal,
		'submission': submission,
		'sender': sender,
	}

	email.send_email('[abp] Proposal Accepted', context, from_email.value, proposal.owner.email, email_text, book=submission, attachment=attachment)

def send_proposal_revisions(proposal, email_text, sender):
	from_email = models.Setting.objects.get(group__name='email', name='from_address')

	context = {
		'base_url': models.Setting.objects.get(group__name='general', name='base_url').value,
		'proposal': proposal,
		'sender': sender,
	}

	email.send_email('[abp] Proposal Revisions Required', context, from_email.value, proposal.owner.email, email_text)


def send_author_sign_off(submission, email_text, sender):
	from_email = models.Setting.objects.get(group__name='email', name='from_address')

	context = {
		'base_url': models.Setting.objects.get(group__name='general', name='base_url').value,
		'submission': submission,
		'sender': sender,
	}

	email.send_email('Book Contract Uploaded', context, from_email.value, submission.owner.email, email_text, book=submission)

def send_copyedit_assignment(submission, copyedit, email_text, sender, attachment=None):
	from_email = models.Setting.objects.get(group__name='email', name='from_address')

	context = {
		'base_url': models.Setting.objects.get(group__name='general', name='base_url').value,
		'submission': submission,
		'copyedit': copyedit,
		'sender': sender,
	}

	email.send_email('Copyedit Assignment', context, from_email.value, copyedit.copyeditor.email, email_text, book=submission, attachment=attachment)

def send_author_invite(submission, copyedit, email_text, sender, attachment=None):
	from_email = models.Setting.objects.get(group__name='email', name='from_address')

	context = {
		'base_url': models.Setting.objects.get(group__name='general', name='base_url').value,
		'submission': submission,
		'copyedit': copyedit,
		'sender': sender,
	}

	email.send_email('Copyediting Completed', context, from_email.value, submission.owner.email, email_text, book=submission, attachment=attachment)

def send_invite_indexer(book, index, email_text, sender, attachment=None):
	from_email = models.Setting.objects.get(group__name='email', name='from_address')
	press_name = models.Setting.objects.get(group__name='general', name='press_name').value

	context = {
		'base_url': models.Setting.objects.get(group__name='general', name='base_url').value,
		'submission': book,
		'index': index,
		'sender': sender,
		'press_name':press_name,
	}

	email.send_email('Indexing Request', context, from_email.value, index.indexer.email, email_text, book=book, attachment=attachment)

def send_invite_typesetter(book, typeset, email_text, sender, attachment=None):

	from_email = models.Setting.objects.get(group__name='email', name='from_address')

	context = {
		'base_url': models.Setting.objects.get(group__name='general', name='base_url').value,
		'submission': typeset.book,
		'typeset': typeset,
		'sender': sender,
	}

	email.send_email('Typesetting', context, from_email.value, typeset.typesetter.email, email_text, book=book, attachment=attachment)

def send_book_editors(book, added_editors,removed_editors,email_text):
	from_email = models.Setting.objects.get(group__name='email', name='from_address')
	base_url = models.Setting.objects.get(group__name='general', name='base_url').value

	context = {
		'base_url':base_url,
		'submission': book,
		'added_editors': added_editors,
		'removed_editors':removed_editors,
		'submission_page': "http://%s/editor/submission/%s/" % (base_url, book.id)
	}
	if added_editors or removed_editors:
		email.send_email('Book Editors have been updated', context, from_email.value, book.owner.email, email_text, book=book)

def send_requests_revisions(book, revision, email_text):
	from_email = models.Setting.objects.get(group__name='email', name='from_address')
	base_url = models.Setting.objects.get(group__name='general', name='base_url').value
	press_name = models.Setting.objects.get(group__name='general', name='press_name').value


	context = {
		'book': book,
		'revision': revision,
		'press_name': press_name,
		'revision_url': "http://%s/revisions/%s" % (base_url, revision.id)
	}

	email.send_email('Revisions Requested', context, from_email.value, book.owner.email, email_text, book=book)
