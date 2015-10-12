from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils import timezone

from revisions import models
from core.files import handle_file_update,handle_attachment,handle_file
from revisions import forms
from core import models as core_models
from core import log
from core.decorators import is_book_editor, is_book_editor_or_author, is_reviewer
from revisions import logic

import os
import mimetypes
import mimetypes as mime
from uuid import uuid4

@login_required
def revision(request, revision_id, submission_id=None):
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

def editor_view_revisions(request, revision_id):
	revision = get_object_or_404(models.Revision, pk=revision_id, completed__isnull=False, book__press_editors__in=[request.user])

	template = 'revisions/editor_view_revisions.html'
	context = {
		'revision': revision,
	}

	return render(request, template, context)

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
