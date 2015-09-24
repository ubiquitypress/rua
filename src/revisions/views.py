from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils import timezone

from revisions import models
from workflow.views import handle_file_update
from revisions import forms
from core import models as core_models
from core import log
from core.decorators import is_book_editor, is_book_editor_or_author, is_reviewer
from revisions import logic

import os
import mimetypes
import mimetypes as mime
from uuid import uuid4

@is_book_editor
def request_revisions(request, submission_id, returner):
	book = get_object_or_404(core_models.Book, pk=submission_id)
	email_text = core_models.Setting.objects.get(group__name='email', name='request_revisions').value
	form = forms.RevisionForm()

	if models.Revision.objects.filter(book=book, completed__isnull=True, revision_type=returner):
		messages.add_message(request, messages.WARNING, 'There is already an outstanding revision request for this book.')

	if request.POST:
		form = forms.RevisionForm(request.POST)
		if form.is_valid():
			new_revision_request = form.save(commit=False)
			new_revision_request.book = book
			new_revision_request.revision_type = returner
			new_revision_request.requestor = request.user
			new_revision_request.save()

			email_text = request.POST.get('id_email_text')
			logic.send_requests_revisions(book, new_revision_request, email_text)
			log.add_log_entry(book, request.user, 'revisions', '%s %s requested revisions for %s' % (request.user.first_name, request.user.last_name, book.title), 'Revisions Requested')

			if returner == 'submission':
				return redirect(reverse('view_new_submission', kwargs={'submission_id': submission_id}))
			elif returner == 'review':
				return redirect(reverse('view_review', kwargs={'submission_id': submission_id}))

	template = 'revisions/request_revisions.html'
	context = {
		'book': book,
		'form': form,
		'email_text': email_text,
	}

	return render(request, template, context)


@login_required
def revision(request, revision_id):
	revision = get_object_or_404(models.Revision, pk=revision_id, book__owner=request.user, completed__isnull=True)

	form = forms.AuthorRevisionForm(instance=revision)

	if request.POST:
		form = forms.AuthorRevisionForm(request.POST, instance=revision)
		if form.is_valid():
			revision = form.save(commit=False)
			revision.completed = timezone.now()
			revision.save()
			task = core_models.Task(book=revision.book, creator=request.user, assignee=revision.requestor, text='Revisions submitted for %s' % revision.book.title, workflow=revision.revision_type, )
			task.save()
			print task
			messages.add_message(request, messages.SUCCESS, 'Revisions recorded, thanks.')
			return redirect(reverse('user_home'))

	template = 'revisions/revision.html'
	context = {
		'revision': revision,
		'form': form,
	}

	return render(request, template, context)

@is_book_editor
def editor_view_revisions(request, revision_id):
	revision = get_object_or_404(models.Revision, pk=revision_id, completed__isnull=False)

	template = 'revisions/editor_view_revisions.html'
	context = {
		'revision': revision,
	}

	return render(request, template, context)

@is_book_editor_or_author
def update_file(request, revision_id, file_id):
	revision = get_object_or_404(models.Revision, pk=revision_id, book__owner=request.user)
	book = revision.book
	_file = get_object_or_404(core_models.File, pk=file_id)

	if request.POST:
		for file in request.FILES.getlist('update_file'):
			handle_file_update(file, _file, book, _file.kind, request.user)
			messages.add_message(request, messages.INFO, 'File updated.')

		return redirect(reverse('revision', kwargs={'revision_id': revision.id}))

	template = 'workflow/update_file.html'
	context = {
		'submission': book,
		'file': _file,
	}

	return render(request, template, context)
