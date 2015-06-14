import json
import os
from uuid import uuid4
import mimetypes as mime

from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.urlresolvers import reverse

from core import models as core_models
from core import views as core_views
from core import forms as core_forms
from review import forms
from review import models

@login_required
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



@login_required
def review(request, review_type, submission_id, access_key=None):

	# Check that this review is being access by the user, is not completed and has not been declined.
	if access_key:
		review_assignment = get_object_or_404(core_models.ReviewAssignment, access_key=access_key, completed__isnull=True, declined__isnull=True)
		submission = get_object_or_404(core_models.Book, pk=submission_id)
	else:
		submission = get_object_or_404(core_models.Book, pk=submission_id)
		review_assignment = get_object_or_404(core_models.ReviewAssignment, user=request.user, book=submission, completed__isnull=True, declined__isnull=True)

	form = forms.GeneratedForm(form=submission.review_form)
	recommendation_form = core_forms.RecommendationForm()

	if request.POST:
		form = forms.GeneratedForm(request.POST, request.FILES, form=submission.review_form)
		if form.is_valid():
			save_dict = {}
			file_fields = models.FormElement.objects.filter(form=submission.review_form, field_type='upload')
			data_fields = models.FormElement.objects.filter(~Q(field_type='upload'), form=submission.review_form)

			for field in file_fields:
				if field.name in request.FILES:
					# TODO change value from string to list [value, value_type]
					save_dict[field.name] = [handle_review_file(request.FILES[field.name], submission, review_assignment, 'review')]

			for field in data_fields:
				if field.name in request.POST:
					# TODO change value from string to list [value, value_type]
					save_dict[field.name] = [request.POST.get(field.name), 'text']

			json_data = json.dumps(save_dict)
			form_results = models.FormResult(form=submission.review_form, data=json_data)
			form_results.save()

			if request.FILES.get('review_file_upload'):
				handle_review_file(request.FILES.get('review_file_upload'), submission, review_assignment, 'review')

			review_assignment.completed = timezone.now()
			if not review_assignment.accepted:
				review_assignment.accepted = timezone.now()
			review_assignment.recommendation = request.POST.get('recommendation')
			review_assignment.results = form_results
			review_assignment.save()

			return redirect(reverse('review_complete', kwargs={'review_type': 'internal', 'submission_id': submission.id}))


	template = 'review/review.html'
	context = {
		'review_assignment': review_assignment,
		'submission': submission,
		'form': form,
		'form_info': submission.review_form,
		'recommendation_form': recommendation_form,
	}

	return render(request, template, context)

def review_complete(request, review_type, submission_id):

	submission = get_object_or_404(core_models.Book, pk=submission_id)
	review_assignment = get_object_or_404(core_models.ReviewAssignment, user=request.user, book=submission)

	template = 'review/complete.html'
	context = {
		'submission': submission,
		'review_assignment': review_assignment,
		'form_info': submission.review_form,
	}

	return render(request,template, context)

def handle_review_file(file, book, review_assignment, kind):

	original_filename = str(file._get_name())
	filename = str(uuid4()) + '.' + str(original_filename.split('.')[1])
	folder_structure = os.path.join(settings.BASE_DIR, 'files', 'books', str(book.id), 'review')

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

	new_file = core_models.File(
		mime_type=file_mime,
		original_filename=original_filename,
		uuid_filename=filename,
		stage_uploaded=1,
		kind=kind,
	)
	new_file.save()
	review_assignment.files.add(new_file)

	return path