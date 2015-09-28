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
from core.decorators import is_book_editor
from core.cache import cache_result
from typeset import forms
from workflow import logic

from pprint import pprint

@is_book_editor
def assign_typesetter(request, submission_id):
	book = get_object_or_404(models.Book, pk=submission_id)
	typesetters = models.User.objects.filter(profile__roles__slug='typesetter')

	if request.POST:
		typesetter_list = User.objects.filter(pk__in=request.POST.getlist('typesetter'))
		file_list = models.File.objects.filter(pk__in=request.POST.getlist('file'))
		due_date = request.POST.get('due_date')
		email_text = request.POST.get('message')

		for typesetter in typesetter_list:
			logic.handle_typeset_assignment(book, typesetter, file_list, due_date, email_text, requestor=request.user)

		return redirect(reverse('view_production', kwargs={'submission_id': submission_id}))

	template = 'workflow/production/assign_typesetter.html'
	context = {
		'submission': book,
		'typesetters': typesetters,
		'email_text': models.Setting.objects.get(group__name='email', name='typeset_request'),
	}

	return render(request, template, context)

@is_book_editor
def view_typesetter(request, submission_id, typeset_id):
	book = get_object_or_404(models.Book, pk=submission_id)
	typeset = get_object_or_404(models.TypesetAssignment, pk=typeset_id)
	email_text = models.Setting.objects.get(group__name='email', name='author_typeset_request').value

	author_form = forms.TypesetAuthorInvite(instance=typeset)
	if typeset.editor_second_review:
		author_form = forms.TypesetTypesetterInvite(instance=typeset)
		email_text = models.Setting.objects.get(group__name='email', name='typesetter_typeset_request').value

	if request.POST and 'invite_author' in request.POST:
		if not typeset.completed:
			messages.add_message(request, messages.WARNING, 'This typeset has not been completed, you cannot invite the author to review.')
			return redirect(reverse('view_typesetter', kwargs={'submission_id': submission_id, 'typeset_id': typeset_id}))
		else:
			typeset.editor_review = timezone.now()
			typeset.save()

	elif request.POST and 'invite_typesetter' in request.POST:
		typeset.editor_second_review = timezone.now()
		typeset.save()
		return redirect(reverse('view_typesetter', kwargs={'submission_id': submission_id, 'typeset_id': typeset_id}))

	elif request.POST and 'send_invite_typesetter' in request.POST:
		author_form = forms.TypesetTypesetterInvite(request.POST, instance=typeset)
		if author_form.is_valid():
			author_form.save()
			typeset.typesetter_invited = timezone.now()
			typeset.save()
			email_text = request.POST.get('email_text')
			logic.send_invite_typesetter(book, typeset, email_text, request.user)
		return redirect(reverse('view_typesetter', kwargs={'submission_id': submission_id, 'typeset_id': typeset_id}))

	elif request.POST and 'send_invite_author' in request.POST:
		author_form = forms.TypesetAuthorInvite(request.POST, instance=typeset)
		if author_form.is_valid():
			author_form.save()
			typeset.author_invited = timezone.now()
			typeset.save()
			email_text = request.POST.get('email_text')
			logic.send_author_invite(book, typeset, email_text, request.user)
		return redirect(reverse('view_typesetter', kwargs={'submission_id': submission_id, 'typeset_id': typeset_id}))

	template = 'workflow/production/view_typeset.html'
	context = {
		'submission': book,
		'typeset': typeset,
		'author_form': author_form,
		'email_text': email_text,
	}

	return render(request, template, context)