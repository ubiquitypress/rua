import json
import os
from uuid import uuid4
import mimetypes as mime
from docx import Document
from docx.shared import Inches
from pprint import pprint
import mimetypes

from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import Http404, HttpResponse, StreamingHttpResponse, HttpResponseRedirect

from core import models as core_models
from core import views as core_views
from core import forms as core_forms
from core.decorators import is_reviewer
from core import log
from core import models as core_models
from review import forms
from review import models
from submission import models as submission_models

@is_reviewer
def reviewer_dashboard(request):

	template = 'review/dashboard.html'
	context = {	
	'pending_tasks': core_models.ReviewAssignment.objects.filter(user=request.user,completed__isnull=True,declined__isnull=True),
	'completed_tasks': core_models.ReviewAssignment.objects.filter(user=request.user,completed__isnull=False),
	}

	return render(request, template, context)

@is_reviewer
def reviewer_decision(request, review_type, submission_id, review_assignment, decision=None):

	# Check the review assignment as not been completed and is being accessed by the assigned user
	submission = get_object_or_404(core_models.Book, pk=submission_id)
	review_assignment = get_object_or_404(core_models.ReviewAssignment, pk=review_assignment, user=request.user, completed__isnull=True, declined__isnull=True, accepted__isnull=True)

	if decision and decision == 'accept':
		review_assignment.accepted = timezone.now()
	elif decision and decision == 'decline':
		review_assignment.declined = timzeone.now()

	# If we didn't get a decision above, offer the user a choice.
	if request.POST:
		if 'accept' in request.POST:
			review_assignment.accepted = timezone.now()
		elif 'decline' in request.POST:
			review_assignment.declined = timezone.now()

	if request.POST or decision:
		review_assignment.save()
		if review_assignment.accepted:
			return redirect(reverse('review_without_access_key', kwargs={'review_type': review_type, 'submission_id': submission.pk}))
		elif review_assignment.declined:
			return redirect(reverse('user_home'))

	template = 'review/reviewer_decision.html'
	context = {
		'submission': submission,
		'review_assignment': review_assignment,
	}

	return render(request, template, context)



@is_reviewer
def review(request, review_type, submission_id, access_key=None):

	ci_required = core_models.Setting.objects.get(group__name='general', name='ci_required')

	# Check that this review is being access by the user, is not completed and has not been declined.
	if access_key:
		review_assignment = get_object_or_404(core_models.ReviewAssignment, access_key=access_key, completed__isnull=True, declined__isnull=True, review_type=review_type)
		submission = get_object_or_404(core_models.Book, pk=submission_id)
	elif review_type == 'proposal':
		submission = get_object_or_404(submission_models.Proposal, pk=submission_id)
		review_assignment = get_object_or_404(submission_models.ProposalReview, user=request.user, proposal=submission, completed__isnull=True, declined__isnull=True)
	else:
		submission = get_object_or_404(core_models.Book, pk=submission_id)
		review_assignment = get_object_or_404(core_models.ReviewAssignment, user=request.user, book=submission, completed__isnull=True, declined__isnull=True, review_type=review_type)

	form = forms.GeneratedForm(form=submission.review_form)
	recommendation_form = core_forms.RecommendationForm(ci_required=ci_required.value)

	if not request.POST and request.GET.get('download') == 'docx':
		path = create_review_form(submission)
		return serve_file(request, path)

	if request.POST:
		form = forms.GeneratedForm(request.POST, request.FILES, form=submission.review_form)
		recommendation_form = core_forms.RecommendationForm(request.POST, ci_required=ci_required.value)
		if form.is_valid() and recommendation_form.is_valid():
			save_dict = {}
			file_fields = models.FormElement.objects.filter(form=submission.review_form, field_type='upload')
			data_fields = models.FormElement.objects.filter(~Q(field_type='upload'), form=submission.review_form)

			for field in file_fields:
				if field.name in request.FILES:
					# TODO change value from string to list [value, value_type]
					save_dict[field.name] = [handle_review_file(request.FILES[field.name], submission, review_assignment, 'reviewer')]

			for field in data_fields:
				if field.name in request.POST:
					# TODO change value from string to list [value, value_type]
					save_dict[field.name] = [request.POST.get(field.name), 'text']

			json_data = json.dumps(save_dict)
			form_results = models.FormResult(form=submission.review_form, data=json_data)
			form_results.save()

			if request.FILES.get('review_file_upload'):
				handle_review_file(request.FILES.get('review_file_upload'), submission, review_assignment, 'reviewer')

			review_assignment.completed = timezone.now()
			if not review_assignment.accepted:
				review_assignment.accepted = timezone.now()
			review_assignment.recommendation = request.POST.get('recommendation')
			review_assignment.competing_interests = request.POST.get('competing_interests')
			review_assignment.results = form_results
			review_assignment.save()

			if not review_type == 'proposal':
				log.add_log_entry(book=submission, user=request.user, kind='review', message='Reviewer %s %s completed review.' % (review_assignment.user.first_name, review_assignment.user.last_name), short_name='Review Assignment')

			return redirect(reverse('review_complete', kwargs={'review_type': review_type, 'submission_id': submission.id}))


	template = 'review/review.html'
	context = {
		'review_assignment': review_assignment,
		'submission': submission,
		'form': form,
		'form_info': submission.review_form,
		'recommendation_form': recommendation_form,
	}

	return render(request, template, context)

@is_reviewer
def review_complete(request, review_type, submission_id):

	if review_type == 'proposal':
		submission = get_object_or_404(submission_models.Proposal, pk=submission_id)
		review_assignment = get_object_or_404(submission_models.ProposalReview, user=request.user, proposal=submission)
	else:
		submission = get_object_or_404(core_models.Book, pk=submission_id)
		review_assignment = get_object_or_404(core_models.ReviewAssignment, user=request.user, book=submission, review_type=review_type)

	template = 'review/complete.html'
	context = {
		'submission': submission,
		'review_assignment': review_assignment,
		'form_info': submission.review_form,
	}

	return render(request,template, context)

def render_choices(choices):
	c_split = choices.split('|')
	return [(choice.capitalize(), choice) for choice in c_split]

def create_review_form(submission):
	document = Document()
	document.add_heading(submission.title, 0)
	p = document.add_paragraph('You should complete this form and then use the review page to upload it.')
	relations = models.FormElementsRelationship.objects.filter(form=submission.review_form)
	for relation in relations:

		if relation.element.field_type in ['text', 'textarea', 'date', 'email']:
			document.add_heading(relation.element.name, level=1)
			document.add_paragraph(relation.help_text).italic = True

		if relation.element.field_type in ['select', 'check']:
			document.add_heading(relation.element.name, level=1)
			if relation.element.field_type == 'select':
				choices = render_choices(relation.element.choices)
			else:
				choices = ['Y', 'N']

			p = document.add_paragraph(relation.help_text)
			p.add_run(' Mark your choice however you like, as long as it is clear.').italic = True
			table = document.add_table(rows=2, cols=len(choices))
			hdr_cells = table.rows[0].cells
			for i, choice in enumerate(choices):
				hdr_cells[i].text = choice[0]
			table.style = 'TableGrid'

	document.add_page_break()
	path = os.path.join(settings.BASE_DIR, 'files', 'forms', '%s.docx' % str(uuid4()))

	document.save(path)
	return path

@is_reviewer
def serve_file(request, file_path):
	try:
		fsock = open(file_path, 'r')
		mimetype = mimetypes.guess_type(file_path)
		response = StreamingHttpResponse(fsock, content_type=mimetype)
		response['Content-Disposition'] = "attachment; filename=review_form.docx"
		pprint(response)
		return response
	except IOError:
		messages.add_message(request, messages.ERROR, 'File not found.')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def handle_review_file(file, book, review_assignment, kind):

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

	print(file_mime)

	try:
		file_mime = file_mime[0]
		if not file_mime:
			file_mime = 'unknown'
	except IndexError:
		file_mime = 'unknown'

	new_file = core_models.File(
		mime_type=file_mime,
		original_filename=original_filename,
		uuid_filename=filename,
		stage_uploaded=1,
		kind=kind,
		owner=review_assignment.user,
	)
	new_file.save()
	review_assignment.files.add(new_file)

	return path