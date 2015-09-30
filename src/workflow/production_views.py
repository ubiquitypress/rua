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
from workflow import forms
from workflow.views import handle_file, handle_file_update
from typeset import forms as typeset_forms

from pprint import pprint

## PRODUCTION ##

@is_book_editor
def view_production(request, submission_id):
	book = get_object_or_404(models.Book, pk=submission_id)
	typeset_assignments = models.TypesetAssignment.objects.filter(book=book)

	if request.POST and request.GET.get('start', None):
		if request.GET.get('start') == 'typesetting':
			book.stage.typesetting = timezone.now()
			book.stage.save()

	template = 'workflow/production/view.html'
	context = {
		'active': 'production',
		'submission': book,
		'format_list': models.Format.objects.filter(book=book).select_related('file'),
		'chapter_list': models.Chapter.objects.filter(book=book).select_related('file'),
		'typeset_assignments': typeset_assignments,
	}

	return render(request, template, context)

@is_book_editor
def catalog(request, submission_id):
	book = get_object_or_404(models.Book, pk=submission_id)

	internal_review_assignments = models.ReviewAssignment.objects.filter(book=book, review_type='internal', completed__isnull=False).select_related('user', 'review_round')
	external_review_assignments = models.ReviewAssignment.objects.filter(book=book, review_type='external', completed__isnull=False).select_related('user', 'review_round')

	metadata_form = forms.EditMetadata(instance=book)
	cover_form = forms.CoverForm(instance=book)

	if request.POST:
		if request.GET.get('metadata', None):
			metadata_form = forms.EditMetadata(request.POST, instance=book)

			if metadata_form.is_valid():
				metadata_form.save()

				for keyword in book.keywords.all():
					book.keywords.remove(keyword)

				for keyword in request.POST.getlist('tags'):
					new_keyword, c = models.Keyword.objects.get_or_create(name=keyword)
					book.keywords.add(new_keyword)
				book.save()
				return redirect(reverse('catalog', kwargs={'submission_id': submission_id}))

		if request.GET.get('cover', None):
			cover_form = forms.CoverForm(request.POST, request.FILES, instance=book)

			if cover_form.is_valid():
				cover_form.save()
				return redirect(reverse('catalog', kwargs={'submission_id': submission_id}))

	template = 'workflow/production/catalog.html'
	context = {
		'active': 'production',
		'submission': book,
		'metadata_form': metadata_form,
		'cover_form': cover_form,
		'internal_review_assignments': internal_review_assignments,
		'external_review_assignments': external_review_assignments,
	}

	return render(request, template, context)

@is_book_editor
def identifiers(request, submission_id, identifier_id=None):
	book = get_object_or_404(models.Book, pk=submission_id)

	if identifier_id:
		identifier = get_object_or_404(models.Identifier, pk=identifier_id)

		if request.GET.get('delete', None) == 'true':
			identifier.delete()
			return redirect(reverse('identifiers', kwargs={'submission_id': submission_id}))

		form = forms.IdentifierForm(instance=identifier)
	else:
		identifier = None
		form = forms.IdentifierForm()

	if request.POST:
		if identifier_id:
			form = forms.IdentifierForm(request.POST, instance=identifier)
		else:
			form = forms.IdentifierForm(request.POST)

		if form.is_valid():
			new_identifier = form.save(commit=False)
			new_identifier.book = book
			new_identifier.save()

			return redirect(reverse('identifiers', kwargs={'submission_id': submission_id}))

	template = 'workflow/production/identifiers.html'
	context = {
		'submission': book,
		'identifier': identifier,
		'form': form,
	}

	return render(request, template, context)

@is_book_editor
def update_contributor(request, submission_id, contributor_type, contributor_id=None):
	book = get_object_or_404(models.Book, pk=submission_id)

	if contributor_id:
		if contributor_type == 'author':
			contributor = get_object_or_404(models.Author, pk=contributor_id)
			form = submission_forms.AuthorForm(instance=contributor)
		elif contributor_type == 'editor':
			contributor = get_object_or_404(models.Editor, pk=contributor_id)
			form = submission_forms.EditorForm(instance=contributor)
	else:
		contributor = None
		if contributor_type == 'author':
			form = submission_forms.AuthorForm()
		elif contributor_type == 'editor':
			form = submission_forms.EditorForm()


	if request.POST:
		if contributor:
			if contributor_type == 'author':
				form = submission_forms.AuthorForm(request.POST, instance=contributor)
			elif contributor_type == 'editor':
				form = submission_forms.EditorForm(request.POST, instance=contributor)
		else:
			if contributor_type == 'author':
				form = submission_forms.AuthorForm(request.POST)
			elif contributor_type == 'editor':
				form = submission_forms.EditorForm(request.POST)

		if form.is_valid():
			saved_contributor = form.save()

			if not contributor:
				if contributor_type == 'author':
					book.author.add(saved_contributor)
				elif contributor_type == 'editor':
					book.editor.add(saved_contributor)

		return redirect(reverse('catalog', kwargs={'submission_id': submission_id}))

	template = 'workflow/production/update_contributor.html'
	context = {
		'submission': book,
		'form': form,
		'contributor': contributor,
	}

	return render(request, template, context)

@is_book_editor
def delete_contributor(request, submission_id, contributor_type, contributor_id):
	book = get_object_or_404(models.Book, pk=submission_id)

	if contributor_id:
		if contributor_type == 'author':
			contributor = get_object_or_404(models.Author, pk=contributor_id)
		elif contributor_type == 'editor':
			contributor = get_object_or_404(models.Editor, pk=contributor_id)

		contributor.delete()

		return redirect(reverse('catalog', kwargs={'submission_id': submission_id}))

@is_book_editor
def add_format(request, submission_id):
	book = get_object_or_404(models.Book, pk=submission_id)
	format_form = forms.FormatForm()

	if request.POST:
		format_form = forms.FormatForm(request.POST, request.FILES)
		if format_form.is_valid():
			new_file = handle_file(request.FILES.get('format_file'), book, 'format', request.user)
			new_format = format_form.save(commit=False)
			new_format.book = book
			new_format.file = new_file
			new_format.save()
			log.add_log_entry(book=book, user=request.user, kind='production', message='%s %s loaded a new format, %s' % (request.user.first_name, request.user.last_name, new_format.identifier), short_name='New Format Loaded')
			return redirect(reverse('view_production', kwargs={'submission_id': book.id}))

	template = 'workflow/production/add_format.html'
	context = {
		'submission': book,
		'format_form': format_form,
	}

	return render(request, template, context)

@is_book_editor
def add_chapter(request, submission_id):
	book = get_object_or_404(models.Book, pk=submission_id)
	chapter_form = forms.ChapterForm()

	if request.POST:
		chapter_form = forms.ChapterForm(request.POST, request.FILES)
		if chapter_form.is_valid():
			new_file = handle_file(request.FILES.get('chapter_file'), book, 'chapter', request.user)
			new_chapter = chapter_form.save(commit=False)
			new_chapter.book = book
			new_chapter.file = new_file
			new_chapter.save()
			log.add_log_entry(book=book, user=request.user, kind='production', message='%s %s loaded a new chapter, %s' % (request.user.first_name, request.user.last_name, new_chapter.identifier), short_name='New Chapter Loaded')
			return redirect(reverse('view_production', kwargs={'submission_id': book.id}))

	template = 'workflow/production/add_chapter.html'
	context = {
		'submission': book,
		'chapter_form': chapter_form,
	}

	return render(request, template, context)

@is_book_editor
def delete_format_or_chapter(request, submission_id, format_or_chapter, id):
	book = get_object_or_404(models.Book, pk=submission_id)

	if format_or_chapter == 'chapter':
		item = get_object_or_404(models.Chapter, pk=id)
	elif format_or_chapter == 'format':
		item = get_object_or_404(models.Format, pk=id)

	if item:
		item.file.delete()
		item.delete()
		messages.add_message(request, messages.SUCCESS, 'Item deleted')
	else:
		messages.add_message(request, messages.WARNING, 'Item not found.')

	return redirect(reverse('view_production', kwargs={'submission_id': book.id}))

@is_book_editor
def update_format_or_chapter(request, submission_id, format_or_chapter, id):
	book = get_object_or_404(models.Book, pk=submission_id)

	if format_or_chapter == 'chapter':
		item = get_object_or_404(models.Chapter, pk=id)
	elif format_or_chapter == 'format':
		item = get_object_or_404(models.Format, pk=id)

	form = forms.UpdateChapterFormat()

	if request.POST:
		form = forms.UpdateChapterFormat(request.POST, request.FILES)
		if form.is_valid():
			item.name = request.POST.get('name')
			item.save()
			handle_file_update(request.FILES.get('file'), item.file, book, item.file.kind, request.user)
			return redirect(reverse('view_production', kwargs={'submission_id': book.id}))

	template = 'workflow/production/update.html'
	context = {
		'submission': book,
		'item': item,
		'form': form,
	}

	return render(request, template, context)

## END PRODUCTION ##

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

	author_form = typeset_forms.TypesetAuthorInvite(instance=typeset)
	if typeset.editor_second_review:
		author_form = typeset_forms.TypesetTypesetterInvite(instance=typeset)
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
		author_form = typeset_forms.TypesetTypesetterInvite(request.POST, instance=typeset)
		if author_form.is_valid():
			author_form.save()
			typeset.typesetter_invited = timezone.now()
			typeset.save()
			email_text = request.POST.get('email_text')
			logic.send_invite_typesetter(book, typeset, email_text, request.user)
		return redirect(reverse('view_typesetter', kwargs={'submission_id': submission_id, 'typeset_id': typeset_id}))

	elif request.POST and 'send_invite_author' in request.POST:
		author_form = typeset_forms.TypesetAuthorInvite(request.POST, instance=typeset)
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


@is_book_editor
def retailers(request, submission_id, retailer_id=None):
	book = get_object_or_404(models.Book, pk=submission_id)
	retailers = models.Retailer.objects.filter(book=book)
	form = forms.RetailerForm()

	if retailer_id:
		retailer = get_object_or_404(models.Retailer, pk=retailer_id)
		form = forms.RetailerForm(instance=retailer)

	if request.GET.get('delete', None):
		retailer.delete()
		return redirect(reverse('retailers', kwargs={'submission_id': submission_id}))

	if request.POST:
		if retailer_id:
			form = forms.RetailerForm(request.POST, instance=retailer)
			message = 'Retailer updated.'
		else:
			form = forms.RetailerForm(request.POST)
			message = 'New retailer added.'

		if form.is_valid():
			new_retailer = form.save(commit=False)
			new_retailer.book = book
			new_retailer.save()

			messages.add_message(request, messages.INFO, message)
			
			return redirect(reverse('retailers', kwargs={'submission_id': submission_id}))

	template = 'workflow/production/retailers.html'
	context = {
		'submission': book,
		'retailers': retailers,
		'form': form,
		'retailer_id': retailer_id,
	}

	return render(request, template, context)

