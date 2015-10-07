from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import logout as logout_user
from django.contrib.auth import login as login_user
from django.shortcuts import redirect, render, get_object_or_404
from django.http import Http404, HttpResponse, StreamingHttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from django.db import IntegrityError
from django.conf import settings

from core import models
from core import log
from core import email
from core.decorators import is_editor, is_book_editor, is_book_editor_or_author
from core.cache import cache_result
from revisions import models as revisions_models
from review import models as review_models
from workflow import logic
from manager import models as manager_models
from workflow import forms
from submission import models as submission_models
from submission import forms as submission_forms

from pprint import pprint
import os
import mimetypes
import mimetypes as mime
from uuid import uuid4
import json

@is_book_editor
def dashboard(request):

	if request.POST:
		order = request.POST.get('order')
		filterby = request.POST.get('filter')
		search = request.POST.get('search')
	else:
		filterby = None
		search = None
		order = 'title'

	print search

	query_list = []

	if filterby:
		query_list.append(Q(stage__current_stage=filterby))

	if search:
		query_list.append(Q(title__contains=search) | Q(subtitle__contains=search) | Q(prefix__contains=search))

	if filterby:
		book_list = models.Book.objects.filter(publication_date__isnull=True).filter(*query_list).order_by(order)
	else:
		book_list = models.Book.objects.filter(publication_date__isnull=True).order_by(order)

	print filterby
	print order

	template = 'workflow/dashboard.html'
	context = {
		'book_list': book_list,
		'recent_activity': models.Log.objects.all().order_by('-date_logged')[:15],
		'notifications': models.Task.objects.filter(assignee=request.user, completed__isnull=True).order_by('due'),
		'order': order,
		'filterby': filterby,
	}

	return render(request, template, context)

@is_editor
def new_submissions(request):

	submission_list = models.Book.objects.filter(stage__current_stage='submission')

	template = 'workflow/new_submissions.html'
	context = {
		'submission_list': submission_list,
		'active': 'new',
	}

	return render(request, template, context)

@is_book_editor
def view_new_submission(request, submission_id):

	submission = get_object_or_404(models.Book, pk=submission_id)

	if request.POST and 'review' in request.POST:
		logic.create_new_review_round(submission)
		submission.stage.review = timezone.now()
		submission.stage.current_stage = 'review'
		submission.stage.save()

		if submission.stage.current_stage == 'review':
			log.add_log_entry(book=submission, user=request.user, kind='review', message='Submission moved to Review', short_name='Submission in Review')

		messages.add_message(request, messages.SUCCESS, 'Submission has been moved to the review stage.')

		return redirect(reverse('view_review', kwargs={'submission_id': submission.id}))


	template = 'workflow/new/view_new_submission.html'
	context = {
		'submission': submission,
		'active': 'new',
		'revision_requests': revisions_models.Revision.objects.filter(book=submission, revision_type='submission')
	}

	return render(request, template, context)

@is_book_editor
def decline_submission(request, submission_id):

	submission = get_object_or_404(models.Book, pk=submission_id)

	if request.POST and 'decline' in request.POST:
		submission.stage.declined = timezone.now()
		submission.stage.current_stage = 'declined'
		submission.stage.save()
		messages.add_message(request, messages.SUCCESS, 'Submission declined.')
		return redirect(reverse('user_home'))

	template = 'workflow/decline_submission.html'
	context = {
		'submission': submission,
	}

	return render(request, template, context)

@is_editor
def in_review(request):

	submission_list = models.Book.objects.filter(stage__current_stage='review')

	template = 'workflow/in_review.html'
	context = {
		'submission_list': submission_list,
		'active': 'review',
	}

	return render(request, template, context)

@is_editor
def in_editing(request):

	submission_list = models.Book.objects.filter(stage__current_stage='editing')

	template = 'workflow/in_editing.html'
	context = {
		'submission_list': submission_list,
		'active': 'editing',
	}

	return render(request, template, context)

@is_editor
def in_production(request):

	submission_list = models.Book.objects.filter(stage__current_stage='production')

	template = 'workflow/in_production.html'
	context = {
		'submission_list': submission_list,
		'active': 'production',
	}

	return render(request, template, context)

@is_book_editor
def view_review(request, submission_id):

	submission = get_object_or_404(models.Book, pk=submission_id)
	review_rounds = models.ReviewRound.objects.filter(book=submission).order_by('-round_number')
	internal_review_assignments = models.ReviewAssignment.objects.filter(book=submission, review_type='internal').select_related('user', 'review_round')
	external_review_assignments = models.ReviewAssignment.objects.filter(book=submission, review_type='external').select_related('user', 'review_round')

	template = 'workflow/review/view_review.html'
	context = {
		'submission': submission,
		'active': 'review',
		'internal_review_assignments': internal_review_assignments,
		'external_review_assignments': external_review_assignments,
		'review_rounds': review_rounds,
		'revision_requests': revisions_models.Revision.objects.filter(book=submission, revision_type='review')
	}

	return render(request, template, context)

@is_book_editor
def add_review_files(request, submission_id, review_type):
	submission = get_object_or_404(models.Book, pk=submission_id)

	if request.POST:
		files = models.File.objects.filter(pk__in=request.POST.getlist('file'))
		for file in files:
			if review_type == 'internal':
				submission.internal_review_files.add(file)
			else:
				submission.external_review_files.add(file)

		messages.add_message(request, messages.SUCCESS, '%s files added to Review' % files.count())

		return redirect(reverse('view_review', kwargs={'submission_id': submission.id}))

	template = 'workflow/review/add_review_files.html'
	context = {
		'submission': submission,
	}

	return render(request, template, context)

@is_book_editor
def delete_review_files(request, submission_id, review_type, file_id):
	submission = get_object_or_404(models.Book, pk=submission_id)
	file = get_object_or_404(models.File, pk=file_id)

	if review_type == 'internal':
		submission.internal_review_files.remove(file)
	else:
		submission.external_review_files.remove(file)

	return redirect(reverse('view_review', kwargs={'submission_id': submission.id}))

@is_book_editor
def add_reviewers(request, submission_id, review_type, round_number):

	submission = get_object_or_404(models.Book, pk=submission_id)
	reviewers = models.User.objects.filter(profile__roles__slug='reviewer')
	review_forms = review_models.Form.objects.all()
	committees = manager_models.Group.objects.filter(group_type='review_committee')
	review_round = get_object_or_404(models.ReviewRound, book=submission, round_number=round_number)

	if request.POST:
		reviewers = User.objects.filter(pk__in=request.POST.getlist('reviewer'))
		committees = manager_models.Group.objects.filter(pk__in=request.POST.getlist('committee'))
		review_form = review_models.Form.objects.get(ref=request.POST.get('review_form'))
		due_date = request.POST.get('due_date')
		email_text = request.POST.get('message')

		if request.FILES.get('attachment'):
			attachment = handle_file(request.FILES.get('attachment'), submission, 'misc', request.user)
		else:
			attachment = None

		# Handle reviewers
		for reviewer in reviewers:
			logic.handle_review_assignment(submission, reviewer, review_type, due_date, review_round, request.user, email_text, attachment)

		# Handle committees
		for committee in committees:
			members = manager_models.GroupMembership.objects.filter(group=committee)
			for member in members:
				logic.handle_review_assignment(submission, member.user, review_type, due_date, review_round, request.user, email_text, attachment)

		# Tidy up and save
		if review_type == 'internal' and not submission.stage.internal_review:
			submission.stage.internal_review = timezone.now()
			submission.stage.save()
			log.add_log_entry(book=submission, user=request.user, kind='review', message='Internal Review Started', short_name='Submission entered Internal Review')

		elif review_type == 'external' and not submission.stage.external_review:
			submission.stage.external_review = timezone.now()
			submission.stage.save()
			log.add_log_entry(book=submission, user=request.user, kind='review', message='External Review Started', short_name='Submission entered External Review')

		submission.review_form = review_form
		submission.save()

		return redirect(reverse('view_review', kwargs={'submission_id': submission.id}))

	template = 'workflow/review/add_reviewers.html'
	context = {
		'reviewers': reviewers,
		'committees': committees,
		'active': 'new',
		'email_text': models.Setting.objects.get(group__name='email', name='review_request'),
		'review_forms': review_forms,
	}

	return render(request, template, context)

@is_book_editor
def view_review_assignment(request, submission_id, assignment_id):

	submission = get_object_or_404(models.Book, pk=submission_id)
	review_assignment = get_object_or_404(models.ReviewAssignment, pk=assignment_id)
	result = review_assignment.results
	relations = review_models.FormElementsRelationship.objects.filter(form=result.form)
	data_ordered = logic.order_data(logic.decode_json(result.data), relations)

	template = 'workflow/review/review_assignment.html'
	context = {
		'submission': submission,
		'review': review_assignment,
		'data_ordered': data_ordered,
		'result': result,
		'active': 'review',
	}

	return render(request, template, context)

@is_book_editor
def add_review_round(request, submission_id):
	'creates a new review round'
	submission = get_object_or_404(models.Book, pk=submission_id)
	logic.create_new_review_round(submission)
	messages.add_message(request, messages.SUCCESS, 'New review round started')
	return redirect(reverse('view_review', kwargs={'submission_id':submission_id}))

@is_book_editor
def move_to_editing(request, submission_id):
	'Moves a submission to the editing stage'
	submission = get_object_or_404(models.Book, pk=submission_id)
	if not submission.stage.editing:
		log.add_log_entry(book=submission, user=request.user, kind='editing', message='Submission moved to Editing.', short_name='Submission in Editing')
	submission.stage.editing = timezone.now()
	submission.stage.current_stage = 'editing'
	submission.stage.save()

	return redirect(reverse('view_editing', kwargs={'submission_id': submission_id}))

# Log
@is_book_editor
def view_log(request, submission_id):
	book = get_object_or_404(models.Book, pk=submission_id)
	log_list = models.Log.objects.filter(book=book).order_by('-date_logged')
	email_list = models.EmailLog.objects.filter(book=book).order_by('-sent')

	template = 'workflow/log.html'
	context = {
		'submission': book,
		'log_list': log_list,
		'email_list': email_list,
		'active': 'log',
	}

	return render(request, template, context)

## PROPOSALS ##

@is_editor
def proposal(request):
	proposal_list = submission_models.Proposal.objects.exclude(status='declined').exclude(status='accepted')

	template = 'workflow/proposals/proposal.html'
	context = {
		'proposal_list': proposal_list,
	}

	return render(request, template, context)

@is_editor
def view_proposal(request, proposal_id):
	proposal = get_object_or_404(submission_models.Proposal, pk=proposal_id)
	relationships = models.ProposalFormElementsRelationship.objects.filter(form=proposal.form)
	data = json.loads(proposal.data)

	template = 'workflow/proposals/view_proposal.html'
	context = {
		'proposal': proposal,
		'relationships':relationships,
		'data':data,
	}

	return render(request, template, context)

@is_editor
def start_proposal_review(request, proposal_id):
	proposal = get_object_or_404(submission_models.Proposal, pk=proposal_id, date_review_started__isnull=True)
	reviewers = models.User.objects.filter(profile__roles__slug='reviewer')
	committees = manager_models.Group.objects.filter(group_type='review_committee')
	start_form = submission_forms.ProposalStart()

	if request.POST:
		start_form = submission_forms.ProposalStart(request.POST, instance=proposal)
		if start_form.is_valid():
			proposal = start_form.save(commit=False)
			proposal.date_review_started = timezone.now()
			due_date = request.POST.get('due_date')
			email_text = models.Setting.objects.get(group__name='email', name='proposal_review_request').value
			reviewers = User.objects.filter(pk__in=request.POST.getlist('reviewer'))
			committees = manager_models.Group.objects.filter(pk__in=request.POST.getlist('committee'))

			# Handle reviewers
			for reviewer in reviewers:
				new_review_assignment = submission_models.ProposalReview(
					user=reviewer,
					proposal=proposal,
					due=due_date,
				)

				try:
					new_review_assignment.save()
					proposal.review_assignments.add(new_review_assignment)
					send_proposal_review_request(proposal, new_review_assignment, email_text)
				except IntegrityError:
					messages.add_message(request, messages.WARNING, '%s %s is already a reviewer' % (reviewer.first_name, reviewer.last_name))

			# Handle committees
			for committee in committees:
				members = manager_models.GroupMembership.objects.filter(group=committee)
				for member in members:
					new_review_assignment = submission_models.ProposalReview(
						user=member.user,
						proposal=proposal,
						due=due_date,
					)

					try:
						new_review_assignment.save()
						proposal.review_assignments.add(new_review_assignment)
						send_proposal_review_request(proposal, new_review_assignment, email_text)
					except IntegrityError:
						messages.add_message(request, messages.WARNING, '%s %s is already a reviewer' % (member.user.first_name, member.user.last_name))

			# Tidy up and save

			proposal.date_review_started = timezone.now()
			proposal.save()

			return redirect(reverse('view_proposal', kwargs={'proposal_id': proposal.id}))

	template = 'workflow/proposals/start_proposal_review.html'
	context = {
		'proposal': proposal,
		'start_form': start_form,
		'reviewers': reviewers,
		'committees': committees,
	}

	return render(request, template, context)

@is_editor
def view_proposal_review(request, submission_id, assignment_id):

	submission = get_object_or_404(submission_models.Proposal, pk=submission_id)
	review_assignment = get_object_or_404(submission_models.ProposalReview, pk=assignment_id)
	result = review_assignment.results
	if result:
		relations = review_models.FormElementsRelationship.objects.filter(form=result.form)
		data_ordered = logic.order_data(logic.decode_json(result.data), relations)
	else:
		relations = None
		data_ordered = None

	template = 'workflow/review/review_assignment.html'
	context = {
		'submission': submission,
		'review': review_assignment,
		'data_ordered': data_ordered,
		'result': result,
		'active': 'proposal_review',
	}

	return render(request, template, context)

@is_editor
def add_proposal_reviewers(request, proposal_id):

	proposal = get_object_or_404(submission_models.Proposal, pk=proposal_id)
	reviewers = models.User.objects.filter(profile__roles__slug='reviewer')
	committees = manager_models.Group.objects.filter(group_type='review_committee')

	if request.POST:
		due_date = request.POST.get('due_date')
		email_text = models.Setting.objects.get(group__name='email', name='proposal_review_request').value
		reviewers = User.objects.filter(pk__in=request.POST.getlist('reviewer'))
		committees = manager_models.Group.objects.filter(pk__in=request.POST.getlist('committee'))

		# Handle reviewers
		for reviewer in reviewers:
			new_review_assignment = submission_models.ProposalReview(
				user=reviewer,
				proposal=proposal,
				due=due_date,
			)

			try:
				new_review_assignment.save()
				proposal.review_assignments.add(new_review_assignment)
				send_proposal_review_request(proposal, new_review_assignment, email_text)
			except IntegrityError:
				messages.add_message(request, messages.WARNING, '%s %s is already a reviewer' % (reviewer.first_name, reviewer.last_name))

		# Handle committees
		for committee in committees:
			members = manager_models.GroupMembership.objects.filter(group=committee)
			for member in members:
				new_review_assignment = submission_models.ProposalReview(
					user=reviewer,
					proposal=proposal,
					due=due_date,
				)

				try:
					new_review_assignment.save()
					proposal.review_assignments.add(new_review_assignment)
					send_proposal_review_request(proposal, new_review_assignment, email_text)
				except IntegrityError:
					messages.add_message(request, messages.WARNING, '%s %s is already a reviewer' % (member.user.first_name, member.user.last_name))

		# Tidy up and save

		proposal.date_review_started = timezone.now()
		proposal.save()

		return redirect(reverse('view_proposal', kwargs={'proposal_id': proposal.id}))

	template = 'workflow/proposals/add_reviewers.html'
	context = {
		'proposal': proposal,
		'reviewers': reviewers,
		'committees': committees,
	}

	return render(request, template, context)

@is_editor
def decline_proposal(request, proposal_id):

	proposal = get_object_or_404(submission_models.Proposal, pk=proposal_id)
	email_text = models.Setting.objects.get(group__name='email', name='proposal_decline').value

	if request.POST:
		proposal.status = 'declined'
		logic.close_active_reviews(proposal)
		proposal.save()
		logic.send_proposal_decline(proposal, email_text=request.POST.get('decline-email'), sender=request.user)
		return redirect(reverse('proposals'))

	template = 'workflow/proposals/decline_proposal.html'
	context = {
		'proposal': proposal,
		'email_text': email_text,
	}

	return render(request, template, context)


@is_editor
def accept_proposal(request, proposal_id):
	'Marks a proposal as accepted, creates a submission and emails the user'
	proposal = get_object_or_404(submission_models.Proposal, pk=proposal_id)
	email_text = models.Setting.objects.get(group__name='email', name='proposal_accept').value

	if request.POST:
		proposal.status = 'accepted'
		logic.close_active_reviews(proposal)
		submission = logic.create_submission_from_proposal(proposal, proposal_type=request.POST.get('proposal-type'))
		attachment = handle_attachment(request, submission)
		logic.send_proposal_accept(proposal, email_text=request.POST.get('accept-email'), submission=submission, sender=request.user, attachment=attachment)
		proposal.save()
		return redirect(reverse('proposals'))

	template = 'workflow/proposals/accept_proposal.html'
	context = {
		'proposal': proposal,
		'email_text': email_text,
	}

	return render(request, template, context)

@is_editor
def request_proposal_revisions(request, proposal_id):

	proposal = get_object_or_404(submission_models.Proposal, pk=proposal_id)
	email_text = models.Setting.objects.get(group__name='email', name='proposal_request_revisisons').value

	if request.POST:
		proposal.status = 'revisions_required'
		logic.close_active_reviews(proposal)
		logic.send_proposal_revisions(proposal, email_text=request.POST.get('revisions-email'), sender=request.user)
		proposal.save()
		return redirect(reverse('proposals'))

	template = 'workflow/proposals/revisions_proposal.html'
	context = {
		'proposal': proposal,
		'email_text': email_text,
	}

	return render(request, template, context)

## END PROPOSAL ##

## CONTRACTS ##

@is_book_editor
def contract_manager(request, submission_id, contract_id=None):
	submission = get_object_or_404(models.Book, pk=submission_id)
	action = 'normal'
	if contract_id:
		new_contract_form = forms.UploadContract(instance=submission.contract)
		action = 'edit'
	else:
		new_contract_form = forms.UploadContract()

	if request.POST:
		if contract_id:
			new_contract_form = forms.UploadContract(request.POST, request.FILE, instance=submission.contract)
		else:
			new_contract_form = forms.UploadContract(request.POST, request.FILES)
		if new_contract_form.is_valid():
			new_contract = new_contract_form.save(commit=False)

			author_file = request.FILES.get('contract_file')
			new_file = handle_file(author_file, submission, 'contract', request.user)

			new_contract.editor_file = new_file
			new_contract.save()
			submission.contract = new_contract
			submission.save()

			if not new_contract.author_signed_off:
				email_text = models.Setting.objects.get(group__name='email', name='contract_author_sign_off').value
				logic.send_author_sign_off(submission, email_text, sender=request.user)

			if contract_id:
				_kwargs = {'submission_id': submission.id, 'contract_id': contract_id}
			else:
				_kwargs = {'submission_id': submission.id}

			return redirect(reverse('contract_manager', kwargs=_kwargs))

	template = 'workflow/contract/contract_manager.html'
	context = {
		'submission': submission,
		'new_contract_form': new_contract_form,
		'action': action,
	}

	return render(request, template, context)

@is_book_editor
def upload_misc_file(request, submission_id):

	submission = get_object_or_404(models.Book, pk=submission_id)
	if request.POST:
		file_form = forms.UploadMiscFile(request.POST)
		if file_form.is_valid():
			new_file = handle_file(request.FILES.get('misc_file'), submission, file_form.cleaned_data.get('file_type'), request.user, file_form.cleaned_data.get('label'))
			submission.misc_files.add(new_file)
			return redirect(reverse('view_new_submission', kwargs={'submission_id': submission.id}))
	else:
		file_form = forms.UploadMiscFile()

	template = 'workflow/misc_files/upload.html'
	context = {
		'submission': submission,
		'file_form': file_form,
	}

	return render(request, template, context)

## END CONTRACTS ##

# File Handlers - should this be in Core?
@is_book_editor_or_author
def serve_file(request, submission_id, file_id):
	book = get_object_or_404(models.Book, pk=submission_id)
	_file = get_object_or_404(models.File, pk=file_id)
	file_path = os.path.join(settings.BOOK_DIR, submission_id, _file.uuid_filename)

	print file_path

	try:
		fsock = open(file_path, 'r')
		mimetype = mimetypes.guess_type(file_path)
		response = StreamingHttpResponse(fsock, content_type=mimetype)
		response['Content-Disposition'] = "attachment; filename=%s" % (_file.uuid_filename)
		log.add_log_entry(book=book, user=request.user, kind='file', message='File %s downloaded.' % _file.uuid_filename, short_name='Download')
		return response
	except IOError:
		messages.add_message(request, messages.ERROR, 'File not found. %s' % (file_path))
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@is_book_editor_or_author
def serve_versioned_file(request, submission_id, revision_id):
	book = get_object_or_404(models.Book, pk=submission_id)
	versions_file = get_object_or_404(models.FileVersion, pk=revision_id)
	file_path = os.path.join(settings.BOOK_DIR, submission_id, versions_file.uuid_filename)

	try:
		fsock = open(file_path, 'r')
		mimetype = mimetypes.guess_type(file_path)
		response = StreamingHttpResponse(fsock, content_type=mimetype)
		response['Content-Disposition'] = "attachment; filename=%s" % (versions_file.uuid_filename)
		log.add_log_entry(book=book, user=request.user, kind='file', message='File %s downloaded.' % versions_file.uuid_filename, short_name='Download')
		return response
	except IOError:
		messages.add_message(request, messages.ERROR, 'File not found. %s/%s' % (file_path, versions_file.uuid_filename))
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@is_book_editor_or_author
def delete_file(request, submission_id, file_id, returner):
	book = get_object_or_404(models.Book, pk=submission_id)
	_file = get_object_or_404(models.File, pk=file_id)
	file_id = _file.id
	_file.delete()

	if returner == 'new':
		return redirect(reverse('view_new_submission', kwargs={'submission_id': book.id}))
	elif returner == 'review':
		return redirect(reverse('view_review', kwargs={'submission_id': book.id}))

@is_book_editor_or_author
def update_file(request, submission_id, file_id, returner):
	book = get_object_or_404(models.Book, pk=submission_id)
	_file = get_object_or_404(models.File, pk=file_id)

	if request.POST:
		for file in request.FILES.getlist('update_file'):
			handle_file_update(file, _file, book, _file.kind, request.user)
			messages.add_message(request, messages.INFO, 'File updated.')

		if returner == 'new':
			return redirect(reverse('view_new_submission', kwargs={'submission_id': book.id}))

	template = 'workflow/update_file.html'
	context = {
		'submission': book,
		'file': _file,
	}

	return render(request, template, context)

@is_book_editor_or_author
def versions_file(request, submission_id, file_id):
	book = get_object_or_404(models.Book, pk=submission_id)
	_file = get_object_or_404(models.File, pk=file_id)
	versions = models.FileVersion.objects.filter(file=_file)

	template = 'workflow/versions_file.html'
	context = {
		'submission': book,
		'file': _file,
		'versions': versions
	}

	return render(request, template, context)

## File helpers
def handle_file_update(file, old_file, book, kind, owner):

	original_filename = str(file._get_name())
	filename = str(uuid4()) + str(os.path.splitext(original_filename)[1])
	folder_structure = os.path.join(settings.BASE_DIR, 'files', 'books', str(book.id))

	if not os.path.exists(folder_structure):
		os.makedirs(folder_structure)

	path = os.path.join(folder_structure, str(filename))
	fd = open(path, 'wb')
	for chunk in file.chunks():
		fd.write(chunk)
	fd.close()

	file_mime = mime.guess_type(filename)

	try:
		file_mime = file_mime[0]
	except IndexError:
		file_mime = 'unknown'


	new_version = models.FileVersion(
		file=old_file,
		original_filename=old_file.original_filename,
		uuid_filename=old_file.uuid_filename,
		date_uploaded=old_file.date_uploaded,
		owner=old_file.owner,
	)

	new_version.save()

	old_file.mime_type=file_mime
	old_file.original_filename=original_filename
	old_file.uuid_filename=filename
	old_file.date_uploaded=timezone.now
	old_file.owner=owner
	old_file.save()

	return path

## File helpers
def handle_file(file, book, kind, owner, label=None):

	original_filename = str(file._get_name())
	filename = str(uuid4()) + str(os.path.splitext(original_filename)[1])
	folder_structure = os.path.join(settings.BASE_DIR, 'files', 'books', str(book.id))

	if not os.path.exists(folder_structure):
		os.makedirs(folder_structure)

	path = os.path.join(folder_structure, str(filename))
	fd = open(path, 'wb')
	for chunk in file.chunks():
		fd.write(chunk)
	fd.close()

	file_mime = mime.guess_type(filename)

	try:
		file_mime = file_mime[0]
	except IndexError:
		file_mime = 'unknown'

	if not file_mime:
		file_mime = 'unknown'

	new_file = models.File(
		mime_type=file_mime,
		original_filename=original_filename,
		uuid_filename=filename,
		stage_uploaded=1,
		kind=kind,
		label=label,
		owner=owner
	)
	new_file.save()

	return new_file

def handle_attachment(request, submission):
	if request.FILES.get('attachment_file'):
		attachment_file = request.FILES.get('attachment_file')
		return handle_file(attachment_file, submission, 'misc', request.user)
	else:
		return None

# Email handler - should be moved to logic!
def send_proposal_review_request(proposal, review_assignment, email_text):
	from_email = models.Setting.objects.get(group__name='email', name='from_address')
	base_url = models.Setting.objects.get(group__name='general', name='base_url')

	review_url = 'http://%s/review/%s/%s/' % (base_url.value, 'proposal', proposal.id)

	context = {
		'review': review_assignment,
		'review_url': review_url,
	}

	email.send_email('Proposal Review Request', context, from_email.value, review_assignment.user.email, email_text)
