from django.contrib.auth import authenticate
from django.contrib.auth import logout as logout_user
from django.contrib.auth import login as login_user
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from submission import forms
from core import models as core_models

import mimetypes as mime
from uuid import uuid4
import os

@login_required
def start_submission(request, book_id=None):

	if book_id:
		book = get_object_or_404(core_models.Book, pk=book_id, owner=request.user)
		book_form = forms.SubmitBookStageOne(instance=book)
	else:
		book = None
		book_form = forms.SubmitBookStageOne()

	if request.method == 'POST':
		if book:
			book_form = forms.SubmitBookStageOne(request.POST, instance=book)
		else:
			book_form = forms.SubmitBookStageOne(request.POST)
		if book_form.is_valid():
			book = book_form.save(commit=False)
			book.owner = request.user
			book.submission_stage = 2
			book.save()
			return redirect(reverse('submission_two', kwargs={'book_id': book.id}))

	template = "submission/start_submission.html"
	context = {
		'book_form': book_form,
		'book': book,
		'active': 1,
	}

	return render(request, template, context)

@login_required
def submission_two(request, book_id):
	book = get_object_or_404(core_models.Book, pk=book_id, owner=request.user)
	book_form = forms.SubmitBookStageTwo(instance=book)

	if request.method == 'POST':
		book_form = forms.SubmitBookStageTwo(request.POST, instance=book)
		if book_form.is_valid():
			book = book_form.save(commit=False)
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

	if request.method == 'POST':
		if 'manuscript_upload' in request.POST:
			for file in request.FILES.getlist('manuscript_file'):
				handle_file(file, book, 'manuscript')

		if 'additional_upload' in request.POST:
			print request.FILES.getlist('additional_file')
			for file in request.FILES.getlist('additional_file'):
				handle_file(file, book, 'additional')

		if 'next_stage' in request.POST:
			book.submission_stage = 4
			book.save()
			return redirect(reverse('submission_four', kwargs={'book_id': book.id}))

		# Catch, after any post we always redirect to avoid someone resubmitting the same file twice.
		return redirect(reverse('submission_three', kwargs={'book_id': book.id}))

	template = 'submission/submission_three.html'
	context = {
		'book': book,
		'active': 3,
		'manuscript_files': manuscript_files,
		'additional_files': additional_files,
	}

	return render(request, template, context)

@login_required
def submission_four(request, book_id):
	book = get_object_or_404(core_models.Book, pk=book_id, owner=request.user)

	template = 'submission/submission_four.html'
	context = {
		'book': book,
		'active': 4,
	}

	return render(request, template, context)

@login_required
def submission_five(request, book_id):
	book = get_object_or_404(core_models.Book, pk=book_id, owner=request.user)

	template = 'submission/submission_three.html'
	context = {
		'book': book,
		'active': 5,
	}

	return render(request, template, context)

@login_required
def start_proposal(request):

	proposal_form = forms.SubmitProposal()

	if request.method == 'POST':
		proposal_form = forms.SubmitProposal(request.POST, request.FILES)
		if proposal_form.is_valid():
			proposal = proposal_form.save(commit=False)
			proposal.owner = request.user
			proposal.save()
			messages.add_message(request, messages.SUCCESS, 'Proposal %s submitted' % proposal.id)
			return redirect(reverse('user_home'))


	template = "submission/start_proposal.html"
	context = {
		'proposal_form': proposal_form,
	}

	return render(request, template, context)


## File helpers
def handle_file(file, book, kind):

	original_filename = str(file._get_name())
	filename = str(uuid4()) + '.' + str(original_filename.split('.')[1])
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

	new_file = core_models.File(
		mime_type=file_mime,
		original_filename=original_filename,
		uuid_filename=filename,
		stage_uploaded=1,
		kind=kind,
	)
	new_file.save()
	book.files.add(new_file)
	book.save()


	return path

# AJAX handler
@csrf_exempt
def file_order(request, book_id, type_to_handle):

	book = get_object_or_404(core_models.Book, pk=book_id, owner=request.user)

	if type_to_handle == 'manuscript':
		id_to_get = 'man'
		files = core_models.File.objects.filter(book=book, kind='manuscript')
	elif type_to_handle == 'additional':
		id_to_get = 'add'
		files = core_models.File.objects.filter(book=book, kind='additional')

	if request.POST:
		ids = request.POST.getlist('%s[]' % id_to_get)
		ids = [int(_id) for _id in ids]
		for file in files:
			# Get the index:
			file.sequence = ids.index(file.id)
			file.save()

	return HttpResponse('Thanks')
