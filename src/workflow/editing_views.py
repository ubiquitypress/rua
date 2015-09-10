from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.models import User

from core import models
from core import log
from core import email
from core.cache import cache_result
from copyedit import forms
from workflow import logic

from pprint import pprint

@staff_member_required
def view_editing(request, submission_id):
	book = get_object_or_404(models.Book, pk=submission_id)

	if request.POST and request.GET.get('start', None):
		action = request.GET.get('start')

		if action == 'copyediting':
			book.stage.copyediting = timezone.now()
			log.add_log_entry(book=book, user=request.user, kind='editing', message='Copyediting has commenced.', short_name='Copyediting Started')
		elif action == 'indexing':
			book.stage.indexing = timezone.now()
			log.add_log_entry(book=book, user=request.user, kind='editing', message='Indexing has commenced.', short_name='Indexing Started')
		elif action == 'production':
			book.stage.production = timezone.now()
			book.stage.current_stage = 'production'
			log.add_log_entry(book=book, user=request.user, kind='production', message='Submission moved to Production', short_name='Submission in Production')
			book.stage.save()
			return redirect(reverse('view_production', kwargs={'submission_id': submission_id}))

		book.stage.save()
		return redirect(reverse('view_editing', kwargs={'submission_id': submission_id}))

	template = 'workflow/editing/view_editing.html'
	context = {
		'submission': book,
		'active': 'editing',
	}

	return render(request, template, context)

@staff_member_required
def assign_copyeditor(request, submission_id):
	book = get_object_or_404(models.Book, pk=submission_id)
	copyeditors = models.User.objects.filter(profile__roles__slug='copyeditor')

	if request.POST:
		copyeditor_list = User.objects.filter(pk__in=request.POST.getlist('copyeditor'))
		file_list = models.File.objects.filter(pk__in=request.POST.getlist('file'))
		due_date = request.POST.get('due_date')
		email_text = request.POST.get('message')

		for copyeditor in copyeditor_list:
			logic.handle_copyeditor_assignment(book, copyeditor, file_list, due_date, email_text, requestor=request.user)
			log.add_log_entry(book=book, user=request.user, kind='editing', message='Copyeditor %s %s assigend to %s' % (copyeditor.first_name, copyeditor.last_name, book.title), short_name='Copyeditor Assigned')

		return redirect(reverse('view_editing', kwargs={'submission_id': submission_id}))

	template = 'workflow/editing/assign_copyeditor.html'
	context = {
		'submission': book,
		'copyeditors': copyeditors,
		'email_text': models.Setting.objects.get(group__name='email', name='copyedit_request'),
	}

	return render(request, template, context)

@staff_member_required
def view_copyedit(request, submission_id, copyedit_id):
	book = get_object_or_404(models.Book, pk=submission_id)
	copyedit = get_object_or_404(models.CopyeditAssignment, pk=copyedit_id)
	author_form = forms.CopyeditAuthorInvite(instance=copyedit)
	email_text = models.Setting.objects.get(group__name='email', name='author_copyedit_request').value

	if request.POST and 'invite_author' in request.POST:
		if not copyedit.completed:
			messages.add_message(request, messages.WARNING, 'This copyedit has not been completed, you cannot invite the author to review.')
			return redirect(reverse('view_copyedit', kwargs={'submission_id': submission_id, 'copyedit_id': copyedit_id}))
		else:
			copyedit.editor_review = timezone.now()
			log.add_log_entry(book=book, user=request.user, kind='editing', message='Copyedit Review Completed by %s %s' % (request.user.first_name, request.user.last_name), short_name='Editor Copyedit Review Complete')
			copyedit.save()

	elif request.POST and 'send_invite_author' in request.POST:
		author_form = forms.CopyeditAuthorInvite(request.POST, instance=copyedit)
		author_form.save()
		copyedit.author_invited = timezone.now()
		copyedit.save()
		email_text = request.POST.get('email_text')
		logic.send_author_invite(book, copyedit, email_text)
		return redirect(reverse('view_copyedit', kwargs={'submission_id': submission_id, 'copyedit_id': copyedit_id}))

	template = 'workflow/editing/view_copyedit.html'
	context = {
		'submission': book,
		'copyedit': copyedit,
		'author_form': author_form,
		'email_text': email_text,
	}

	return render(request, template, context)

@staff_member_required
def assign_indexer(request, submission_id):
	book = get_object_or_404(models.Book, pk=submission_id)
	indexers = models.User.objects.filter(profile__roles__slug='indexer')

	if request.POST:
		indexer_list = User.objects.filter(pk__in=request.POST.getlist('indexer'))
		file_list = models.File.objects.filter(pk__in=request.POST.getlist('file'))
		due_date = request.POST.get('due_date')
		email_text = request.POST.get('message')

		for indexer in indexer_list:
			logic.handle_indexer_assignment(book, indexer, file_list, due_date, email_text, requestor=request.user)
			log.add_log_entry(book=book, user=request.user, kind='editing', message='Indexer %s %s assigend to %s' % (indexer.first_name, indexer.last_name, book.title), short_name='Indexer Assigned')

		return redirect(reverse('view_editing', kwargs={'submission_id': submission_id}))

	template = 'workflow/editing/assign_indexer.html'
	context = {
		'submission': book,
		'indexers': indexers,
		'email_text': models.Setting.objects.get(group__name='email', name='index_request'),
	}

	return render(request, template, context)

@staff_member_required
def view_index(request, submission_id, index_id):
	book = get_object_or_404(models.Book, pk=submission_id)
	index = get_object_or_404(models.IndexAssignment, pk=index_id)

	template = 'workflow/editing/view_index.html'
	context = {
		'submission': book,
		'index': index,
	}

	return render(request, template, context)

