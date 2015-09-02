from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.core.urlresolvers import reverse

from core import models
from core import task
from indexing import forms

import mimetypes as mime
from uuid import uuid4
import os

@login_required
def index(request, submission_id, index_id):
	book = get_object_or_404(models.Book, pk=submission_id)
	index = get_object_or_404(models.IndexAssignment, pk=index_id, indexer=request.user, book=book)

	# if the copyedit is complete, show the completed page.
	if index.completed:
		return redirect(reverse('index_complete', kwargs={'submission_id': submission_id, 'index_id': index_id}))

	form = forms.Index(instance=index)

	if request.POST:
		form = forms.Index(request.POST, instance=index)
		if form.is_valid():
			index = form.save(commit=False)

			for _file in request.FILES.getlist('index_file_upload'):
				new_file = handle_index_file(_file, book, index, 'index')
				index.index_files.add(new_file)

			if not index.accepted:
				index.accepted = timezone.now()
			index.save()
			messages.add_message(request, messages.SUCCESS, 'Indexing completed. Thanks!')
			return redirect(reverse('index_files', kwargs={'submission_id': submission_id, 'index_id': index_id}))


	template = 'indexing/index.html'
	context = {
		'submission': book,
		'index': index,
		'form': form,
	}

	return render(request, template, context)

@login_required
def index_files(request, submission_id, index_id):
	book = get_object_or_404(models.Book, pk=submission_id)
	index = get_object_or_404(models.IndexAssignment, pk=index_id, indexer=request.user, book=book)

	# if the copyedit is complete, show the completed page.
	if index.completed:
		return redirect(reverse('index_complete', kwargs={'submission_id': submission_id, 'index_id': index_id}))

	if request.POST:
		for _file in index.index_files.all():
			_file.label = request.POST.get('label_%s' % _file.id)
			_file.save()
		index.completed = timezone.now()
		index.save()
		new_task = task.create_new_task(book, index.indexer, index.requestor, "Indexing completed for %s" % book.title, workflow='editing')
		return redirect(reverse('index_complete', kwargs={'submission_id': submission_id, 'index_id': index_id}))

	template = 'indexing/index_files.html'
	context = {
		'submission': book,
		'index': index,
	}

	return render(request, template, context)

@login_required
def index_complete(request, submission_id, index_id):
	book = get_object_or_404(models.Book, pk=submission_id)
	index = get_object_or_404(models.IndexAssignment, pk=index_id, indexer=request.user, book=book)

	# If edit not complete, redirect back...
	if not index.completed:
		return redirect(reverse('index', kwargs={'submission_id': submission_id, 'index_id': index_id}))

	template = 'indexing/index_complete.html'
	context = {
		'submission': book,
		'index': index,
	}

	return render(request, template, context)


def handle_index_file(file, book, index, kind):

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
		owner=index.indexer,
	)
	new_file.save()

	return new_file

