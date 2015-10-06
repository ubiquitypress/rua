from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.core.urlresolvers import reverse

from core import models
from core import task
from core import log
from core.decorators import is_copyeditor
from copyedit import forms

import mimetypes as mime
from uuid import uuid4
import os

@is_copyeditor
def copyedit(request, submission_id, copyedit_id):
	book = get_object_or_404(models.Book, pk=submission_id)
	copyedit = get_object_or_404(models.CopyeditAssignment, pk=copyedit_id, copyeditor=request.user, book=book)

	# if the copyedit is complete, show the completed page.
	print copyedit.completed
	#if copyedit.completed:
	#	return redirect(reverse('copyedit_complete', kwargs={'submission_id': submission_id, 'copyedit_id': copyedit_id}))

	form = forms.Copyedit(instance=copyedit)

	if request.POST:
		form = forms.Copyedit(request.POST, instance=copyedit)
		if form.is_valid():
			copyedit = form.save(commit=False)

			for _file in request.FILES.getlist('copyedit_file_upload'):
				new_file = handle_copyedit_file(_file, book, copyedit, 'copyedit')
				copyedit.copyedit_files.add(new_file)

			if not copyedit.accepted:
				copyedit.accepted = timezone.now()
			copyedit.save()
			messages.add_message(request, messages.SUCCESS, 'Copyedit completed. Thanks!')
			return redirect(reverse('copyedit_files', kwargs={'submission_id': submission_id, 'copyedit_id': copyedit_id}))


	template = 'copyedit/copyedit.html'
	context = {
		'submission': book,
		'copyedit': copyedit,
		'form': form,
	}

	return render(request, template, context)

@is_copyeditor
def copyedit_files(request, submission_id, copyedit_id):
	book = get_object_or_404(models.Book, pk=submission_id)
	copyedit = get_object_or_404(models.CopyeditAssignment, pk=copyedit_id, copyeditor=request.user, book=book)

	# if the copyedit is complete, show the completed page.
	if copyedit.completed:
		return redirect(reverse('copyedit_complete', kwargs={'submission_id': submission_id, 'copyedit_id': copyedit_id}))

	if request.POST:
		for _file in copyedit.copyedit_files.all():
			_file.label = request.POST.get('label_%s' % _file.id)
			_file.save()
		copyedit.completed = timezone.now()
		log.add_log_entry(book=book, user=request.user, kind='editing', message='Copyeditor %s %s completed.' % (copyedit.copyeditor.first_name, copyedit.copyeditor.last_name), short_name='Copyeditor Complete')
		copyedit.save()
		new_task = task.create_new_task(book, copyedit.copyeditor, copyedit.requestor, "Copyediting completed for %s" % book.title, workflow='editing')
		return redirect(reverse('copyedit_complete', kwargs={'submission_id': submission_id, 'copyedit_id': copyedit_id}))

	template = 'copyedit/copyedit_files.html'
	context = {
		'submission': book,
		'copyedit': copyedit,
	}

	return render(request, template, context)

@is_copyeditor
def copyedit_author(request, submission_id, copyedit_id):
	book = get_object_or_404(models.Book, pk=submission_id)
	copyedit = get_object_or_404(models.CopyeditAssignment, pk=copyedit_id, book__owner=request.user, book=book, author_invited__isnull=False, author_completed__isnull=True)

	form = forms.CopyeditAuthor(instance=copyedit)

	if request.POST:
		form = forms.CopyeditAuthor(request.POST, instance=copyedit)
		if form.is_valid():
			form.save()
			for _file in request.FILES.getlist('copyedit_file_upload'):
				new_file = handle_copyedit_file(_file, book, copyedit, 'copyedit')
				copyedit.author_files.add(new_file)
				copyedit.author_completed = timezone.now()
				copyedit.save()
				log.add_log_entry(book=book, user=request.user, kind='editing', message='Copyedit Author review compeleted by %s %s.' % (request.user.first_name, request.user.last_name), short_name='Copyedit Author Review Complete')
				messages.add_message(request, messages.SUCCESS, 'Copyedit task complete. Thanks.')
				new_task = task.create_new_task(book, copyedit.book.owner, copyedit.requestor, "Author Copyediting completed for %s" % book.title, workflow='editing')
				return redirect(reverse('user_home'))

	template = 'copyedit/copyedit_author.html'
	context = {
		'submission': book,
		'copyedit': copyedit,
		'form': form,
	}

	return render(request, template, context)

@is_copyeditor
def copyedit_complete(request, submission_id, copyedit_id):
	book = get_object_or_404(models.Book, pk=submission_id)
	copyedit = get_object_or_404(models.CopyeditAssignment, pk=copyedit_id, copyeditor=request.user, book=book)

	# If edit not complete, redirect back...
	if not copyedit.completed:
		return redirect(reverse('copyedit', kwargs={'submission_id': submission_id, 'copyedit_id': copyedit_id}))

	template = 'copyedit/copyedit_complete.html'
	context = {
		'submission': book,
		'copyedit': copyedit,
	}

	return render(request, template, context)


def handle_copyedit_file(file, book, copyedit, kind):

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
		owner=copyedit.copyeditor,
	)
	new_file.save()

	return new_file
