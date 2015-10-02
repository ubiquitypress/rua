from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.urlresolvers import reverse

from core import models
from author import forms
from author import logic
from submission import models as submission_models

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
