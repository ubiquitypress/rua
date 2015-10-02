from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required

from core import models
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
