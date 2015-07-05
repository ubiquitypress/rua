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
from core import forms
from core import log
from core import email
from core.cache import cache_result
from review import models as review_models
from workflow import logic
from manager import models as manager_models

from pprint import pprint
import os
import mimetypes
import mimetypes as mime
from uuid import uuid4

@login_required
def new_submissions(request):

	submission_list = models.Book.objects.filter(stage__current_stage='submission')

	template = 'workflow/new_submissions.html'
	context = {
		'submission_list': submission_list,
		'active': 'new',
	}

	return render(request, template, context)

@login_required
def view_new_submission(request, submission_id):

	submission = get_object_or_404(models.Book, pk=submission_id)
	reviewers = models.User.objects.filter(profile__roles__slug='reviewer')
	review_forms = review_models.Form.objects.all()

	committees = manager_models.Group.objects.filter(group_type='review_committee')

	if request.POST:
		review_type = 'internal'
		files = models.File.objects.filter(pk__in=request.POST.getlist('file'))
		reviewers = User.objects.filter(pk__in=request.POST.getlist('reviewer'))
		committees = manager_models.Group.objects.filter(pk__in=request.POST.getlist('committee'))
		review_form = review_models.Form.objects.get(ref=request.POST.get('review_form'))
		due_date = request.POST.get('due_date')
		email_text = request.POST.get('message')

		# Handle files
		for file in files:
			submission.review_files.add(file)

		# Handle reviewers
		for reviewer in reviewers:
			new_review_assignment = models.ReviewAssignment(
				review_type=review_type,
				user=reviewer,
				book=submission,
				due=due_date,
				access_key=str(uuid4()),
			)

			try:
				new_review_assignment.save()
				submission.review_assignments.add(new_review_assignment)
				log.add_log_entry(book=submission, user=request.user, kind='review', message='Reviewer %s %s assigned.' % (reviewer.first_name, reviewer.last_name), short_name='Review Assignment')
				send_review_request(submission, new_review_assignment, email_text)
			except IntegrityError:
				messages.add_message(request, messages.WARNING, '%s %s is already a reviewer' % (reviewer.first_name, reviewer.last_name))

		# Handle committees
		for committee in committees:
			members = manager_models.GroupMembership.objects.filter(group=committee)
			for member in members:
				new_review_assignment = models.ReviewAssignment(
					review_type=review_type,
					user=member.user,
					book=submission,
					due=due_date,
					access_key = str(uuid4()),
				)

				try:
					new_review_assignment.save()
					submission.review_assignments.add(new_review_assignment)
					log.add_log_entry(book=submission, user=request.user, kind='review', message='Reviewer %s %s assigned.' % (member.user.first_name, member.user.last_name), short_name='Review Assignment')
					send_review_request(submission, new_review_assignment, email_text)
				except IntegrityError:
					messages.add_message(request, messages.WARNING, '%s %s is already a reviewer' % (member.user.first_name, member.user.last_name))



		# Tidy up and save
		submission.stage.internal_review = timezone.now()
		submission.stage.current_stage = 'i_review'
		submission.stage.save()
		submission.review_form = review_form
		submission.save()

		return redirect(reverse('view_review', kwargs={'submission_id': submission.id}))


	template = 'workflow/view_new_submission.html'
	context = {
		'submission': submission,
		'reviewers': reviewers,
		'committees': committees,
		'active': 'new',
		'email_text': models.Setting.objects.get(group__name='email', name='review_request'),
		'review_forms': review_forms,
	}

	return render(request, template, context)

@staff_member_required
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

@login_required
def in_review(request):

	submission_list = models.Book.objects.filter(Q(stage__current_stage='i_review') | Q(stage__current_stage='e_review'))

	template = 'workflow/in_review.html'
	context = {
		'submission_list': submission_list,
		'active': 'review',
	}

	return render(request, template, context)

@login_required
def in_editing(request):

	submission_list = models.Book.objects.filter(stage__current_stage='editing')

	template = 'workflow/in_editing.html'
	context = {
		'submission_list': submission_list,
		'active': 'editing',
	}

	return render(request, template, context)

@login_required
def in_production(request):

	submission_list = models.Book.objects.filter(stage__current_stage='production')

	template = 'workflow/in_production.html'
	context = {
		'submission_list': submission_list,
		'active': 'production',
	}

	return render(request, template, context)

@staff_member_required
def view_review(request, submission_id):

	submission = get_object_or_404(models.Book, pk=submission_id)
	reviewers = models.User.objects.filter(profile__roles__slug='reviewer')
	review_forms = review_models.Form.objects.all()
	committees = manager_models.Group.objects.filter(group_type='review_committee')
	internal_review_assignments = models.ReviewAssignment.objects.filter(book=submission, review_type='internal').select_related('user')
	external_review_assignments = models.ReviewAssignment.objects.filter(book=submission, review_type='external').select_related('user')

	if request.POST:
		review_type = 'external'
		files = models.File.objects.filter(pk__in=request.POST.getlist('file'))
		reviewers = User.objects.filter(pk__in=request.POST.getlist('reviewer'))
		committees = manager_models.Group.objects.filter(pk__in=request.POST.getlist('committee'))
		review_form = review_models.Form.objects.get(ref=request.POST.get('review_form'))
		due_date = request.POST.get('due_date')
		email_text = request.POST.get('message')

		# Handle files
		for file in files:
			submission.review_files.add(file)

		# Handle reviewers
		for reviewer in reviewers:
			new_review_assignment = models.ReviewAssignment(
				review_type=review_type,
				user=reviewer,
				book=submission,
				due=due_date,
				access_key=str(uuid4()),
			)

			try:
				new_review_assignment.save()
				submission.review_assignments.add(new_review_assignment)
				log.add_log_entry(book=submission, user=request.user, kind='review', message='Reviewer %s %s assigned.' % (reviewer.first_name, reviewer.last_name), short_name='Review Assignment')
				send_review_request(submission, new_review_assignment, email_text)
			except IntegrityError:
				messages.add_message(request, messages.WARNING, '%s %s is already a reviewer' % (reviewer.first_name, reviewer.last_name))

		# Handle committees
		for committee in committees:
			members = manager_models.GroupMembership.objects.filter(group=committee)
			for member in members:
				new_review_assignment = models.ReviewAssignment(
					review_type=review_type,
					user=member.user,
					book=submission,
					due=due_date,
					access_key = str(uuid4()),
				)

				try:
					new_review_assignment.save()
					submission.review_assignments.add(new_review_assignment)
					log.add_log_entry(book=submission, user=request.user, kind='review', message='External Reviewer %s %s assigned.' % (member.user.first_name, member.user.last_name), short_name='Review Assignment')
					send_review_request(submission, new_review_assignment, email_text)
				except IntegrityError:
					messages.add_message(request, messages.WARNING, '%s %s is already a reviewer' % (member.user.first_name, member.user.last_name))



		# Tidy up and save
		submission.stage.external_review = timezone.now()
		submission.stage.current_stage = 'e_review'
		submission.stage.save()
		submission.review_form = review_form
		submission.save()

		return redirect(reverse('view_review', kwargs={'submission_id': submission.id}))


	template = 'workflow/view_review.html'
	context = {
		'submission': submission,
		'active': 'review',
		'reviewers': reviewers,
		'committees': committees,
		'email_text': models.Setting.objects.get(group__name='email', name='external_review_request'),
		'review_forms': review_forms,
		'internal_review_assignments': internal_review_assignments,
		'external_review_assignments': external_review_assignments,
	}

	return render(request, template, context)

@staff_member_required
def view_review_assignment(request, submission_id, assignment_id):

	submission = get_object_or_404(models.Book, pk=submission_id)
	review_assignment = get_object_or_404(models.ReviewAssignment, pk=assignment_id)
	result = review_assignment.results
	relations = review_models.FormElementsRelationship.objects.filter(form=result.form)
	data_ordered = logic.order_data(logic.decode_json(result.data), relations)

	template = 'workflow/review_assignment.html'
	context = {
		'submission': submission,
		'review': review_assignment,
		'data_ordered': data_ordered,
		'result': result,
		'active': 'review',
	}

	return render(request, template, context)

def move_to_editing(request, submission_id):
	'Moves a submission to the editing stage'
	submission = get_object_or_404(models.Book, pk=submission_id)
	submission.stage.editing = timezone.now()
	submission.stage.current_stage = 'editing'
	submission.stage.save()

	return redirect(reverse('in_editing'))

# Log
@login_required
def view_log(request, submission_id):
	book = get_object_or_404(models.Book, pk=submission_id)
	log_list = models.Log.objects.filter(book=book)

	template = 'workflow/log.html'
	context = {
		'submission': book,
		'log_list': log_list,
		'active': 'log',
	}

	return render(request, template, context)

@login_required
def view_production(request, submission_id):
	book = get_object_or_404(models.Book, pk=submission_id)

	template = 'workflow/production/view.html'
	context = {
		'active': 'production',
		'submission': book,
	}

	return render(request, template, context)

@login_required
def catalog(request, submission_id):
	book = get_object_or_404(models.Book, pk=submission_id)

	template = 'workflow/production/catalog.html'
	context = {
		'active': 'production',
		'submission': book,
	}

	return render(request, template, context)

# File Handlers - should this be in Core?
@login_required
def serve_file(request, submission_id, file_id):
	book = get_object_or_404(models.Book, pk=submission_id)
	_file = get_object_or_404(models.File, pk=file_id)
	file_path = os.path.join(settings.BOOK_DIR, submission_id, _file.uuid_filename)

	try:
		fsock = open(file_path, 'r')
		mimetype = mimetypes.guess_type(file_path)
		response = StreamingHttpResponse(fsock, content_type=mimetype)
		response['Content-Disposition'] = "attachment; filename=%s" % (_file.uuid_filename)
		log.add_log_entry(book=book, user=request.user, kind='file', message='File %s downloaded.' % _file.uuid_filename, short_name='Download')
		return response
	except IOError:
		messages.add_message(request, messages.ERROR, 'File not found. %s/%s' % (file_path, _file.uuid_filename))
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
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

@login_required
def delete_file(request, submission_id, file_id, returner):
	book = get_object_or_404(models.Book, pk=submission_id)
	_file = get_object_or_404(models.File, pk=file_id)
	file_id = _file.id
	_file.delete()

	if returner == 'new':
		return redirect(reverse('view_new_submission', kwargs={'submission_id': book.id}))

@login_required
def update_file(request, submission_id, file_id, returner):
	book = get_object_or_404(models.Book, pk=submission_id)
	_file = get_object_or_404(models.File, pk=file_id)

	if request.POST:
		for file in request.FILES.getlist('update_file'):
			handle_file_update(file, _file, book, _file.kind)
			messages.add_message(request, messages.INFO, 'File updated.')

		if returner == 'new':
			return redirect(reverse('view_new_submission', kwargs={'submission_id': book.id}))

	template = 'workflow/update_file.html'
	context = {
		'submission': book,
		'file': _file,
	}

	return render(request, template, context)

@login_required
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
def handle_file_update(file, old_file, book, kind):

	original_filename = str(file._get_name())
	filename = str(uuid4()) + '.' + str(original_filename.split('.')[1])
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
		date_uploaded=old_file.date_uploaded
	)

	new_version.save()

	old_file.mime_type=file_mime
	old_file.original_filename=original_filename
	old_file.uuid_filename=filename
	old_file.date_uploaded=timezone.now
	old_file.save()

	return path

# Email handler

def send_review_request(book, review_assignment, email_text):
	from_email = models.Setting.objects.get(group__name='email', name='from_address')
	base_url = models.Setting.objects.get(group__name='general', name='base_url')

	review_url = 'http://%s/review/%s/%s/access_key/%s/' % (base_url.value, review_assignment.review_type, book.id, review_assignment.access_key)
	decision_url = 'http://%s/review/%s/%s/assignment/%s/decision/' % (base_url.value, review_assignment.review_type, book.id, review_assignment.id)

	context = {
		'review': review_assignment,
		'review_url': review_url,
		'decision_url': decision_url,
	}

	email.send_email('[abp] Review Request', context, from_email.value, review_assignment.user.email, email_text)
