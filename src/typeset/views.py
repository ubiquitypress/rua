from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.core.urlresolvers import reverse

from core import models
from core import task
from core import log
from typeset import forms

import mimetypes as mime
from uuid import uuid4
import os

@login_required
def typeset(request, submission_id, typeset_id):
	book = get_object_or_404(models.Book, pk=submission_id)
	typeset = get_object_or_404(models.TypesetAssignment, pk=typeset_id, typesetter=request.user, book=book)

	# if the copyedit is complete, show the completed page.
	if typeset.completed:
		return redirect(reverse('typeset_complete', kwargs={'submission_id': submission_id, 'typeset_id': typeset_id}))

	form = forms.Typeset(instance=typeset)

	if request.POST:
		form = forms.Typeset(request.POST, instance=typeset)
		if form.is_valid():
			typeset = form.save(commit=False)

			for _file in request.FILES.getlist('typeset_file_upload'):
				new_file = handle_typeset_file(_file, book, typeset, 'typeset')
				typeset.typeset_files.add(new_file)

			if not typeset.accepted:
				typeset.accepted = timezone.now()

			typeset.save()
			messages.add_message(request, messages.SUCCESS, 'Typeset completed. Thanks!')
			return redirect(reverse('typeset_files', kwargs={'submission_id': submission_id, 'typeset_id': typeset_id}))


	template = 'typeset/typeset.html'
	context = {
		'submission': book,
		'typeset': typeset,
		'form': form,
	}

	return render(request, template, context)

@login_required
def typeset_files(request, submission_id, typeset_id):
	book = get_object_or_404(models.Book, pk=submission_id)
	typeset = get_object_or_404(models.TypesetAssignment, pk=typeset_id, typesetter=request.user, book=book)

	# if the copyedit is complete, show the completed page.
	if typeset.completed:
		return redirect(reverse('typeset_complete', kwargs={'submission_id': submission_id, 'typeset_id': typeset_id}))

	if request.POST:
		for _file in typeset.typeset_files.all():
			_file.label = request.POST.get('label_%s' % _file.id)
			_file.save()
		typeset.completed = timezone.now()
		log.add_log_entry(book=book, user=request.user, kind='production', message='Typesetter %s %s completed.' % (typeset.typesetter.first_name, typeset.typesetter.last_name), short_name='Typesetter Completed')
		typeset.save()
		new_task = task.create_new_task(book, typeset.typesetter, typeset.requestor, "Typsetting completed for %s" % book.title, workflow='production')
		return redirect(reverse('typeset_complete', kwargs={'submission_id': submission_id, 'typeset_id': typeset_id}))

	template = 'typeset/typeset_files.html'
	context = {
		'submission': book,
		'typeset': typeset,
	}

	return render(request, template, context)

@login_required
def typeset_author(request, submission_id, typeset_id):
	book = get_object_or_404(models.Book, pk=submission_id)
	typeset = get_object_or_404(models.TypesetAssignment, pk=typeset_id, book__owner=request.user, book=book)

	form = forms.TypesetAuthor(instance=typeset)

	if request.POST:
		form = forms.TypesetAuthor(request.POST, instance=typeset)
		if form.is_valid():
			form.save()
			for _file in request.FILES.getlist('typeset_file_upload'):
				new_file = handle_typeset_file(_file, book, typeset, 'typeset')
				typeset.author_files.add(new_file)
				typeset.author_completed = timezone.now()
				typeset.save()
				log.add_log_entry(book=book, user=request.user, kind='production', message='Author Typesetting review %s %s completed.' % (request.user.first_name, request.user.last_name), short_name='Author Typesetting Review Completed')
				messages.add_message(request, messages.SUCCESS, 'Typesetting task complete. Thanks.')
				new_task = task.create_new_task(book, typeset.book.owner, typeset.requestor, "Author Typesetting completed for %s" % book.title, workflow='production')
				return redirect(reverse('user_home'))

	template = 'typeset/typeset_author.html'
	context = {
		'submission': book,
		'typeset': typeset,
		'form': form,
	}

	return render(request, template, context)

@login_required
def typeset_complete(request, submission_id, typeset_id):
	book = get_object_or_404(models.Book, pk=submission_id)
	typeset = get_object_or_404(models.TypesetAssignment, pk=typeset_id, typesetter=request.user, book=book)

	# If edit not complete, redirect back...
	if not typeset.completed:
		return redirect(reverse('typeset', kwargs={'submission_id': submission_id, 'typeset_id': typeset_id}))

	template = 'typeset/typeset_complete.html'
	context = {
		'submission': book,
		'typeset': typeset,
	}

	return render(request, template, context)


@login_required
def typeset_typesetter(request, submission_id, typeset_id):
	book = get_object_or_404(models.Book, pk=submission_id)
	typeset = get_object_or_404(models.TypesetAssignment, pk=typeset_id, typesetter=request.user, book=book, typesetter_completed__isnull=True)

	form = forms.TypesetTypesetter(instance=typeset)

	if request.POST:
		form = forms.TypesetTypesetter(request.POST, instance=typeset)
		if form.is_valid():
			form.save()
			for _file in request.FILES.getlist('typeset_file_upload'):
				new_file = handle_typeset_file(_file, book, typeset, 'typeset')
				typeset.typesetter_files.add(new_file)
				typeset.typesetter_completed = timezone.now()
				typeset.save()
				log.add_log_entry(book=book, user=request.user, kind='production', message='Final Typesetting %s %s completed.' % (request.user.first_name, request.user.last_name), short_name='Final Typesetting Completed')
				messages.add_message(request, messages.SUCCESS, 'Typesetting task complete. Thanks.')
				new_task = task.create_new_task(book, typeset.book.owner, typeset.requestor, "Typesetting completed for %s" % book.title, workflow='production')
				return redirect(reverse('user_home'))

	template = 'typeset/typeset_author.html'
	context = {
		'submission': book,
		'typeset': typeset,
		'form': form,
	}

	return render(request, template, context)


def handle_typeset_file(file, book, typeset, kind):

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
		if not file_mime:
			file_mime = 'unknown'
	except IndexError:
		file_mime = 'unknown'

	new_file = models.File(
		mime_type=file_mime,
		original_filename=original_filename,
		uuid_filename=filename,
		stage_uploaded=1,
		kind=kind,
		owner=typeset.typesetter,
	)
	new_file.save()

	return new_file
