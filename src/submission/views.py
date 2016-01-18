from django.contrib.auth import authenticate, logout as logout_user, login as login_user
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseForbidden
from django.utils import timezone
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.views.decorators.http import require_POST
from jfu.http import upload_receive, UploadResponse, JFUResponse
from django.contrib.auth.models import User
from submission import forms
from core import models as core_models, log, task, logic as core_logic
from submission import logic, models as submission_models
from manager import forms as manager_forms
from  __builtin__ import any as string_any

import mimetypes as mime
from uuid import uuid4
import os
from pprint import pprint
import json

@login_required
def start_submission(request, book_id=None):
	
	direct_submissions =  core_models.Setting.objects.get(group__name='general', name='direct_submissions').value
	if not direct_submissions:
		return redirect(reverse('proposal_start'))

	ci_required = core_models.Setting.objects.get(group__name='general', name='ci_required')
	checklist_items = submission_models.SubmissionChecklistItem.objects.all()

	if book_id:
		book = get_object_or_404(core_models.Book, pk=book_id, owner=request.user)
		book_form = forms.SubmitBookStageOne(instance=book, ci_required=ci_required.value)
		checklist_form = forms.SubmissionChecklist(checklist_items=checklist_items, book=book)
	else:
		book = None
		book_form = forms.SubmitBookStageOne()
		checklist_form = forms.SubmissionChecklist(checklist_items=checklist_items)

	if request.method == 'POST':
		if book:
			book_form = forms.SubmitBookStageOne(request.POST, instance=book, ci_required=ci_required.value)
		else:
			book_form = forms.SubmitBookStageOne(request.POST, ci_required=ci_required.value)

		checklist_form = forms.SubmissionChecklist(request.POST, checklist_items=checklist_items)

		if book_form.is_valid() and checklist_form.is_valid():
			book = book_form.save(commit=False)
			book.owner = request.user
			if not book.submission_stage > 2:
				book.submission_stage = 2
				book.save()
				log.add_log_entry(book, request.user, 'submission', 'Submission Started', 'Submission Started')
			book.save()

			if not book_id and book:
				if book.book_type == 'monograph':
					logic.copy_author_to_submission(request.user, book)
				elif book.book_type == 'edited_volume':
					logic.copy_editor_to_submission(request.user, book)
			return redirect(reverse('submission_two', kwargs={'book_id': book.id}))

	template = "submission/start_submission.html"
	context = {
		'book_form': book_form,
		'checklist_form': checklist_form,
		'suggested_reviewers': core_models.Setting.objects.get(name='suggested_reviewers').value,
		'suggested_reviewers_guide': core_models.Setting.objects.get(name='suggested_reviewers_guide').value,
		'book': book,
		'active': 1,
	}

	return render(request, template, context)

@login_required
def submission_two(request, book_id):
	book = get_object_or_404(core_models.Book, pk=book_id, owner=request.user)
	book_form = forms.SubmitBookStageTwo(instance=book)

	logic.check_stage(book, 2)

	if request.method == 'POST':
		book_form = forms.SubmitBookStageTwo(request.POST, instance=book)
		if book_form.is_valid():
			book = book_form.save(commit=False)
			if not book.submission_stage > 3:
				book.submission_stage = 3

			book.save()
			return redirect(reverse('submission_three', kwargs={'book_id': book.id}))

	template = "submission/submission_two.html"
	context = {
		'book': book,
		'book_form': book_form,
		'active': 2,
	}

	return render(request, template, context)

@login_required
def submission_three(request, book_id):
	book = get_object_or_404(core_models.Book, pk=book_id, owner=request.user)
	manuscript_files = core_models.File.objects.filter(book=book, kind='manuscript')
	additional_files = core_models.File.objects.filter(book=book, kind='additional')

	logic.check_stage(book, 3)

	if request.method == 'POST':
		print request.POST
		if 'next_stage' in request.POST:
			if manuscript_files.count() >= 1:
				if not book.submission_stage > 4:
					book.submission_stage = 4
				logic.handle_book_labels(request.POST, book, kind='manuscript')
				book.save()
				return redirect(reverse('submission_three_additional', kwargs={'book_id': book.id}))
			else:
				messages.add_message(request, messages.ERROR, 'You must upload a Manuscript File.')

		# Catch, after any post we always redirect to avoid someone resubmitting the same file twice.
		return redirect(reverse('submission_three', kwargs={'book_id': book.id}))

	template = 'submission/submission_three.html'
	context = {
		'book': book,
		'active': 3,
		'manuscript_files': manuscript_files,
		'additional_files': additional_files,
		'manuscript_guidelines': core_models.Setting.objects.get(name='manuscript_guidelines').value,
	
	}

	return render(request, template, context)

@login_required
def submission_three_additional(request, book_id):
	book = get_object_or_404(core_models.Book, pk=book_id, owner=request.user)
	additional_files = core_models.File.objects.filter(book=book, kind='additional')

	logic.check_stage(book, 4)

	if request.method == 'POST':
		if not book.submission_stage > 5:
			book.submission_stage = 5
		logic.handle_book_labels(request.POST, book, kind='additional')
		book.save()
		return redirect(reverse('submission_four', kwargs={'book_id': book.id}))

	template = 'submission/submission_three_additional.html'
	context = {
		'book': book,
		'active': 4,
		'additional_files': additional_files,
		'additional_guidelines': core_models.Setting.objects.get(name='additional_files_guidelines').value,

	}

	return render(request, template, context)

@login_required
def submission_additional_files(request, book_id, file_type):
	book = get_object_or_404(core_models.Book, pk=book_id, owner=request.user)

	if file_type == 'additional_files':
		files = core_models.File.objects.filter(book=book, kind='additional')
	elif file_type == 'manuscript_files':
		files = core_models.File.objects.filter(book=book, kind='manuscript')

	if request.POST:
		for _file in files:
			_file.label = request.POST.get('label_%s' % _file.id)
			_file.save()
		return redirect(reverse('submission_three', kwargs={'book_id': book.id}))

	template = 'submission/submission_additional_files.html'
	context = {
		'book': book,
		'files': files,
	}

	return render(request, template, context)

@csrf_exempt
def upload(request, book_id, type_to_handle):

	book = get_object_or_404(core_models.Book, pk=book_id, owner=request.user)
	file = upload_receive(request)
	new_file = handle_file(file, book, type_to_handle, request.user)

	if new_file:

		file_dict = {
			'name' : new_file.uuid_filename,
			'size' : file.size,
			'deleteUrl': reverse('jfu_delete', kwargs = { 'book_id': book_id, 'file_pk': new_file.pk }),
			'url': reverse('serve_file', kwargs = {'submission_id': book_id, 'file_id': new_file.pk }),
			'deleteType': 'POST',
			'ruaId': new_file.pk,
			'original_name': new_file.original_filename,
		}

		return UploadResponse( request, file_dict )

	return HttpResponse('No file')

@csrf_exempt
def upload_delete(request, book_id, file_pk):
	success = True
	try:
		instance = core_models.File.objects.get(pk=file_pk)
		os.unlink('%s/%s/%s' % (settings.BOOK_DIR, book_id, instance.uuid_filename))
		instance.delete()
	except core_models.File.DoesNotExist:
		success = False

	return JFUResponse( request, success )

@login_required
def submission_four(request, book_id):
	book = get_object_or_404(core_models.Book, pk=book_id, owner=request.user)

	logic.check_stage(book, 5)

	if request.method == 'POST' and 'next_stage' in request.POST:
		if book.author.count() >= 1 or book.editor.count() >= 1:
			if not book.submission_stage > 6:
				book.submission_stage = 6
				book.save()
			return redirect(reverse('submission_five', kwargs={'book_id': book.id}))
		else:
			messages.add_message(request, messages.ERROR, 'You must add at least one author or editor.')

	template = 'submission/submission_four.html'
	context = {
		'book': book,
		'active': 5,
	}

	return render(request, template, context)

@login_required
def submission_five(request, book_id):
	book = get_object_or_404(core_models.Book, pk=book_id, owner=request.user)

	logic.check_stage(book, 6)

	if request.method == 'POST' and 'complete' in request.POST:
		book.submission_date = timezone.now()
		book.slug = slugify(book.title)
		stage = core_models.Stage(current_stage='submission', submission=book.submission_date)
		stage.save()
		book.stage = stage
		book.save()
		log.add_log_entry(book, request.user, 'submission', 'Submission of %s completed' % book.title, 'Submission Completed')

		# Send ack email
		press_editors  = core_models.User.objects.filter(profile__roles__slug='press-editor')
		logic.send_acknowldgement_email(book, press_editors)
		return redirect(reverse('author_dashboard'))

	template = 'submission/submission_five.html'
	context = {
		'book': book,
		'active': 6,
		'manuscript_files': core_models.File.objects.filter(book=book, kind='manuscript'),
		'additional_files': core_models.File.objects.filter(book=book, kind='additional'),
	}

	return render(request, template, context)

@login_required
def author(request, book_id, author_id=None):
	book = get_object_or_404(core_models.Book, pk=book_id, owner=request.user)

	if author_id:
		if book.author.filter(pk=author_id).exists():
			author = get_object_or_404(core_models.Author, pk=author_id)
			author_form = forms.AuthorForm(instance=author)
		else:
			return HttpResponseForbidden()
	else:
		author = None
		author_form = forms.AuthorForm()

	if request.method == 'POST':
		if author:
			author_form = forms.AuthorForm(request.POST, instance=author)
		else:
			author_form = forms.AuthorForm(request.POST)
		if author_form.is_valid():
			author = author_form.save(commit=False)
			if not author.sequence:
				author.sequence = 1
			author.save()
			if not author_id:
				book.author.add(author)

			return redirect(reverse('submission_four', kwargs={'book_id': book.id}))

	template = "submission/author.html"
	context = {
		'author_form': author_form,
		'book': book,
	}

	return render(request, template, context)

@login_required
def editor(request, book_id, editor_id=None):
	book = get_object_or_404(core_models.Book, pk=book_id, owner=request.user)

	if editor_id:
		if book.editor.filter(pk=editor_id).exists():
			editor = get_object_or_404(core_models.Editor, pk=editor_id)
			editor_form = forms.EditorForm(instance=editor)
		else:
			return HttpResponseForbidden()
	else:
		editor = None
		editor_form = forms.EditorForm()

	if request.method == 'POST':
		if editor:
			editor_form = forms.EditorForm(request.POST, instance=editor)
		else:
			editor_form = forms.EditorForm(request.POST)
		if editor_form.is_valid():
			editor = editor_form.save(commit=False)
			if not editor.sequence:
				editor.sequence = 1
			editor.save()
			if not editor_id:
				book.editor.add(editor)

			return redirect(reverse('submission_four', kwargs={'book_id': book.id}))

	template = "submission/editor.html"
	context = {
		'author_form': editor_form,
		'book': book,
	}

	return render(request, template, context)

@login_required
def start_proposal(request):
	print request.META
	proposal_form_id = core_models.Setting.objects.get(name='proposal_form').value
	proposal_form = manager_forms.GeneratedForm(form=core_models.ProposalForm.objects.get(pk=proposal_form_id))
	default_fields = manager_forms.DefaultForm()

	if request.method == 'POST':
		proposal_form = manager_forms.GeneratedForm(request.POST,form=core_models.ProposalForm.objects.get(pk=proposal_form_id))
		default_fields = manager_forms.DefaultForm(request.POST)
		if proposal_form.is_valid() and default_fields.is_valid():
			save_dict = {}
			file_fields = core_models.ProposalFormElementsRelationship.objects.filter(form=core_models.ProposalForm.objects.get(pk=proposal_form_id), element__field_type='upload')
			data_fields = core_models.ProposalFormElementsRelationship.objects.filter(~Q(element__field_type='upload'), form=core_models.ProposalForm.objects.get(pk=proposal_form_id))

			for field in file_fields:
				if field.element.name in request.FILES:
					# TODO change value from string to list [value, value_type]
					save_dict[field.element.name] = [handle_proposal_file(request.FILES[field.element.name], submission, review_assignment, 'reviewer')]

			for field in data_fields:
				if field.element.name in request.POST:
					# TODO change value from string to list [value, value_type]
					save_dict[field.element.name] = [request.POST.get(field.element.name), 'text']

			defaults = {field.name: field.value() for field in default_fields}
			json_data = json.dumps(save_dict)
			proposal = submission_models.Proposal(form=core_models.ProposalForm.objects.get(pk=proposal_form_id), data=json_data, owner=request.user, **defaults)
			proposal.save()
			editors = User.objects.filter(profile__roles__slug='press-editor')
			message = "A new  Proposal '%s' with id %s has been submitted by %s ."  % (proposal.title,proposal.pk,request.user.username)
			for editor in editors:
				notification = core_models.Task(assignee=editor,creator=request.user,text=message,workflow='proposal')
				notification.save()

			messages.add_message(request, messages.SUCCESS, 'Proposal %s submitted' % proposal.id)
			email_text = core_models.Setting.objects.get(group__name='email', name='proposal_submission_ack').value
			core_logic.send_proposal_submission_ack(proposal, email_text=email_text, owner=request.user)

			log.add_proposal_log_entry(proposal=proposal,user=request.user, kind='proposal', message='Proposal has been submitted by %s.' % request.user.profile.full_name(), short_name='Proposal Submitted')
	
			return redirect(reverse('user_dashboard',kwargs = {}))


	template = "submission/start_proposal.html"
	context = {
		'proposal_form': proposal_form,
		'default_fields': default_fields
	}

	return render(request, template, context)

@login_required
def proposal_revisions(request, proposal_id):

	proposal = get_object_or_404(submission_models.Proposal, pk=proposal_id, owner=request.user, status='revisions_required')

	proposal_form = manager_forms.GeneratedForm(form=core_models.ProposalForm.objects.get(pk=proposal.form.id))
	default_fields = manager_forms.DefaultForm(initial={'title': proposal.title,'author':proposal.author,'subtitle':proposal.subtitle})
	data = json.loads(proposal.data)
	intial_data={}
	for k,v in data.items():
		intial_data[k] = v[0]

	proposal_form.initial=intial_data
	if request.POST:
		proposal_form = manager_forms.GeneratedForm(request.POST, request.FILES, form=core_models.ProposalForm.objects.get(pk=proposal.form.id))
		default_fields = manager_forms.DefaultForm(request.POST)
		if proposal_form.is_valid() and default_fields.is_valid():

			save_dict = {}
			file_fields = core_models.ProposalFormElementsRelationship.objects.filter(form=core_models.ProposalForm.objects.get(pk=proposal.form.id), element__field_type='upload')
			data_fields = core_models.ProposalFormElementsRelationship.objects.filter(~Q(element__field_type='upload'), form=core_models.ProposalForm.objects.get(pk=proposal.form.id))

			for field in file_fields:
				if field.element.name in request.FILES:
					# TODO change value from string to list [value, value_type]
					save_dict[field.element.name] = [handle_proposal_file(request.FILES[field.element.name], submission, review_assignment, 'reviewer')]

			for field in data_fields:
				if field.element.name in request.POST:
					# TODO change value from string to list [value, value_type]
					save_dict[field.element.name] = [request.POST.get(field.element.name), 'text']

			messages.add_message(request, messages.SUCCESS, 'Revisions for Proposal %s submitted' % proposal.id)
		
			json_data = json.dumps(save_dict)
			proposal = submission_models.Proposal.objects.get(form=core_models.ProposalForm.objects.get(pk=proposal.form.id), owner=request.user,pk=proposal_id)
			proposal.data=json_data
			proposal.status = "revisions_submitted"
			defaults=default_fields.cleaned_data
			proposal.title = defaults.get("title")
			proposal.author = defaults.get("author")
			proposal.subtitle = defaults.get("subtitle")
			proposal.save()
			notification = core_models.Task(assignee=proposal.requestor,creator=request.user,text="Revisions for Proposal '%s' with id %s submitted" % (proposal.title,proposal.id),workflow='proposal')
			notification.save()
			
			update_email_text = core_models.Setting.objects.get(group__name='email', name='proposal_revision_submit_ack').value
			log.add_proposal_log_entry(proposal=proposal,user=request.user, kind='proposal', message='Revisions for Proposal "%s %s" with id %s have been submitted.'%(proposal.title,proposal.subtitle,proposal.pk), short_name='Proposal Revisions Submitted')
			core_logic.send_proposal_update(proposal, email_text=update_email_text, sender=request.user, receiver=proposal.requestor)

			messages.add_message(request, messages.SUCCESS, 'Proposal %s submitted' % proposal.id)
			return redirect(reverse('user_dashboard'))

	template = "submission/start_proposal.html"
	context = {
		'proposal_form': proposal_form,
		'default_fields': default_fields,
		'data':data,
		'revise':True,
	}

	return render(request, template, context)
@login_required
def proposal_view(request, proposal_id):

	proposal = submission_models.Proposal.objects.get(pk=proposal_id)

	if proposal.owner == request.user:
		viewable = True

	proposal_form = manager_forms.GeneratedForm(form=core_models.ProposalForm.objects.get(pk=proposal.form.id))
	default_fields = manager_forms.DefaultForm(initial={'title': proposal.title,'author':proposal.author,'subtitle':proposal.subtitle})
	data = json.loads(proposal.data)
	intial_data={}
	for k,v in data.items():
		intial_data[k] = v[0]

	proposal_form.initial=intial_data
	
	roles = request.user.profile.roles.all()

	if string_any('Editor' in role.name for role in roles):
		viewable = True
		editor = True
		if proposal.requestor and not proposal.requestor == request.user:
			editor = False

		print editor
	else:
		editor = False

	if request.POST and editor:
		proposal_form = manager_forms.GeneratedForm(request.POST, request.FILES, form=core_models.ProposalForm.objects.get(pk=proposal.form.id))
		default_fields = manager_forms.DefaultForm(request.POST)
		if proposal_form.is_valid() and default_fields.is_valid():

			save_dict = {}
			file_fields = core_models.ProposalFormElementsRelationship.objects.filter(form=core_models.ProposalForm.objects.get(pk=proposal.form.id), element__field_type='upload')
			data_fields = core_models.ProposalFormElementsRelationship.objects.filter(~Q(element__field_type='upload'), form=core_models.ProposalForm.objects.get(pk=proposal.form.id))

			for field in file_fields:
				if field.element.name in request.FILES:
					# TODO change value from string to list [value, value_type]
					save_dict[field.element.name] = [handle_proposal_file(request.FILES[field.element.name], submission, review_assignment, 'reviewer')]

			for field in data_fields:
				if field.element.name in request.POST:
					# TODO change value from string to list [value, value_type]
					save_dict[field.element.name] = [request.POST.get(field.element.name), 'text']

			json_data = json.dumps(save_dict)
			proposal = submission_models.Proposal.objects.get(form=core_models.ProposalForm.objects.get(pk=proposal.form.id),pk=proposal_id)
			proposal.data=json_data
			proposal.status = "submission"
			defaults=default_fields.cleaned_data
			proposal.title = defaults.get("title")
			proposal.author = defaults.get("author")
			proposal.subtitle = defaults.get("subtitle")	
			proposal.requestor=request.user
			proposal.save()

			update_email_text = core_models.Setting.objects.get(group__name='email', name='proposal_update_ack').value
			log.add_proposal_log_entry(proposal=proposal,user=request.user, kind='proposal', message='Proposal "%s %s" has been updated.'%(proposal.title,proposal.subtitle), short_name='Proposal Updated')
			core_logic.send_proposal_update(proposal, email_text=update_email_text, sender=request.user, receiver=proposal.owner)
			messages.add_message(request, messages.SUCCESS, 'Proposal %s updated' % proposal.id)
			return redirect(reverse('user_dashboard'))

	template = "submission/view_proposal.html"
	context = {
		'proposal_form': proposal_form,
		'default_fields': default_fields,
		'proposal':proposal,
		'data':data,
		'revise':True,
		'editor': editor,
		'viewable':viewable,
	}

	return render(request, template, context)

## File helpers
def handle_file(file, book, kind, user):

	if file:

		original_filename = str(file._get_name())
		filename = str(uuid4()) + str(os.path.splitext(file._get_name())[1])
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
		except IndexError:
			file_mime = 'unknown'

		if not file_mime:
			file_mime = 'unknown'

		new_file = core_models.File(
			mime_type=file_mime,
			original_filename=original_filename,
			uuid_filename=filename,
			stage_uploaded=1,
			kind=kind,
			owner=user,
		)
		new_file.save()
		book.files.add(new_file)
		book.save()

		return new_file

# AJAX handler
@csrf_exempt
@login_required
def file_order(request, book_id, type_to_handle):

	book = get_object_or_404(core_models.Book, pk=book_id, owner=request.user)

	if type_to_handle == 'manuscript':
		id_to_get = 'man'
		files = core_models.File.objects.filter(book=book, kind='manuscript')
	elif type_to_handle == 'additional':
		id_to_get = 'add'
		files = core_models.File.objects.filter(book=book, kind='additional')
	elif type_to_handle == 'author':
		id_to_get = 'auth'
		files = core_models.Author.objects.filter(book=book)
	elif type_to_handle == 'editor':
		id_to_get = 'edit'
		files = core_models.Editor.objects.filter(book=book)

	if request.POST:
		ids = request.POST.getlist('%s[]' % id_to_get)
		ids = [int(_id) for _id in ids]
		for file in files:
			# Get the index:
			file.sequence = ids.index(file.id)
			file.save()

	return HttpResponse('Thanks')
