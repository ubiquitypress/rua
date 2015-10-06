from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib import messages

from core import models
from author import forms
from author import logic
from submission import models as submission_models
from revisions import models as revision_models, forms as revision_forms
from workflow.views import handle_file_update

@login_required
def author_dashboard(request):

	template = 'author/dashboard.html'
	context = {
		'user_submissions': models.Book.objects.filter(owner=request.user),
		'user_proposals': submission_models.Proposal.objects.filter(owner=request.user),
		'author_tasks': logic.author_tasks(request.user),
	}

	return render(request, template, context)

@login_required
def author_submission(request, submission_id):
	book = get_object_or_404(models.Book, pk=submission_id, owner=request.user)

	template = 'author/submission.html'
	context = {
		'submission': book,
		'active': 'user_submission',
		'author_include': 'author/submission_details.html',
		'submission_files': 'author/submission_files.html'
	}

	return render(request, template, context)

@login_required
def status(request, submission_id):
	book = get_object_or_404(models.Book, pk=submission_id, owner=request.user)

	template = 'author/submission.html'
	context = {
		'submission': book,
		'active': 'user_submission',
		'author_include': 'author/status.html',
		'submission_files': 'shared/messages.html',
		'timeline': logic.build_time_line(book),
	}

	return render(request, template, context)

@login_required
def review(request, submission_id, review_id=None):
	book = get_object_or_404(models.Book, pk=submission_id, owner=request.user)

	if review_id:
		review = get_object_or_404(models.ReviewAssignemnt, pk=submission, book=book)

	template = 'author/submission.html'
	context = {
		'submission': book,
		'author_include': '',
	}

	return render(request, template, context)

@login_required
def tasks(request, submission_id):
	book = get_object_or_404(models.Book, pk=submission_id, owner=request.user)

	template = 'author/submission.html'
	context = {
		'submission': book,
		'tasks': logic.submission_tasks(book, request.user),
		'author_include': 'author/tasks.html',
	}

	return render(request, template, context)

@login_required
def revision(request, revision_id, submission_id):
	revision = get_object_or_404(revision_models.Revision, pk=revision_id, book__owner=request.user, completed__isnull=True)
	book = get_object_or_404(models.Book, pk=submission_id, owner=request.user)

	form = revision_forms.AuthorRevisionForm(instance=revision)

	if request.POST:
		form = revision_forms.AuthorRevisionForm(request.POST, instance=revision)
		if form.is_valid():
			revision = form.save(commit=False)
			revision.completed = timezone.now()
			revision.save()
			task = models.Task(book=revision.book, creator=request.user, assignee=revision.requestor, text='Revisions submitted for %s' % revision.book.title, workflow=revision.revision_type, )
			task.save()
			messages.add_message(request, messages.SUCCESS, 'Revisions recorded, thanks.')
			return redirect(reverse('author_dashboard'))

	template = 'author/submission.html'
	context = {
		'submission': book,
		'revision': revision,
		'form': form,
		'author_include': 'author/revision.html',
	}

	return render(request, template, context)

@login_required
def revise_file(request, submission_id, revision_id, file_id):
	revision = get_object_or_404(revision_models.Revision, pk=revision_id, book__owner=request.user)
	book = revision.book
	_file = get_object_or_404(models.File, pk=file_id)
	form = revision_forms.AuthorRevisionForm(instance=revision)

	if request.POST:
		for file in request.FILES.getlist('update_file'):
			handle_file_update(file, _file, book, _file.kind, request.user)
			messages.add_message(request, messages.INFO, 'File updated.')

		return redirect(reverse('author_revision', kwargs={'submission_id': submission_id, 'revision_id': revision.id}))

	template = 'author/submission.html'
	context = {
		'submission': book,
		'revision': revision,
		'file': _file,
		'author_include': 'author/revision.html',
		'submission_files': 'author/revise_file.html',
		'form': form,
	}

	return render(request, template, context)

@login_required
def author_contract_signoff(request, submission_id, contract_id):
	contract = get_object_or_404(models.Contract, pk=contract_id)
	submission = get_object_or_404(models.Book, pk=submission_id, owner=request.user, contract=contract)

	if request.POST:
		author_signoff_form = forms.AuthorContractSignoff(request.POST, request.FILES)
		if author_signoff_form.is_valid():
			if request.FILES.get('author_file'):
				author_file = request.FILES.get('author_file')
				new_file = handle_file(author_file, submission, 'contract')
				contract.author_file = new_file

			contract.author_signed_off = timezone.now()
			contract.save()
			return redirect(reverse('author_submission', kwargs={'submission_id': submission_id}))
	else:
		author_signoff_form = forms.AuthorContractSignoff()

	template = 'author/author_contract_signoff.html'
	context = {
		'submission': 'submission',
		'contract': 'contract',
		'author_signoff_form': 'author_signoff_form',
	}

	return render(request, template, context)
