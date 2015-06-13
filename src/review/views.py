import json
import os
from uuid import uuid4
import mimetypes as mime

from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from django.conf import settings

from core import models as core_models
from review import forms
from review import models
from core import views as core_views

def review(request, review_type, submission_id, access_key=None):

	if access_key:
		review_assignment = get_object_or_404(core_models.ReviewAssignment, access_key=access_key)
		submission = get_object_or_404(core_models.Book, pk=submission_id)
	else:
		submission = get_object_or_404(core_models.Book, pk=submission_id)
		review_assignment = get_object_or_404(core_models.ReviewAssignment, user=request.user, book=submission)

	form = forms.GeneratedForm(form=submission.review_form)

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
			form_results = models.FormResult(form=submission.review_form, data=json_data, review_assignment=review_assignment)
			form_results.save()

	template = 'review/review.html'
	context = {
		'review_assignment': review_assignment,
		'submission': submission,
		'form': form,
	}

	return render(request, template, context)

def handle_review_file(file, book, review_assignment, kind):

	original_filename = str(file._get_name())
	filename = str(uuid4()) + '.' + str(original_filename.split('.')[1])
	folder_structure = os.path.join(settings.BASE_DIR, 'files', 'books', 'review' str(book.id))

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
	review_assignment.file = new_file
	review_assignment.save()


	return path