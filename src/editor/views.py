from django.shortcuts import redirect, render, get_object_or_404
from core.decorators import is_editor, is_book_editor, is_book_editor_or_author
from django.db.models import Q

from core import models


@is_editor
def editor_dashboard(request):

	if request.POST:
		order = request.POST.get('order')
		filterby = request.POST.get('filter')
		search = request.POST.get('search')
	else:
		filterby = None
		search = None
		order = 'title'

	query_list = []

	if filterby:
		query_list.append(Q(stage__current_stage=filterby))

	if search:
		query_list.append(Q(title__contains=search) | Q(subtitle__contains=search) | Q(prefix__contains=search))

	if filterby:
		book_list = models.Book.objects.filter(publication_date__isnull=True).filter(*query_list).order_by(order)
	else:
		book_list = models.Book.objects.filter(publication_date__isnull=True).order_by(order)

	template = 'editor/dashboard.html'
	context = {
		'book_list': book_list,
		'recent_activity': models.Log.objects.all().order_by('-date_logged')[:15],
		'notifications': models.Task.objects.filter(assignee=request.user, completed__isnull=True).order_by('due'),
		'order': order,
		'filterby': filterby,
	}

	return render(request, template, context)


@is_editor
def editor_submission(request, submission_id):
	book = get_object_or_404(models.Book, pk=submission_id)

	template = 'editor/submission.html'
	context = {
		'submission': book,
		'active': 'user_submission',
		'author_include': 'editor/submission_details.html',
		'submission_files': 'editor/submission_files.html'
	}

	return render(request, template, context)
