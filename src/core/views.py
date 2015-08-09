from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import logout as logout_user
from django.contrib.auth import login as login_user
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core import serializers
from django.conf import settings

from core import models
from core import forms
from workflow import forms as workflow_forms
from submission import models as submission_models

from pprint import pprint
import json
from time import strftime
from uuid import uuid4
import os
import mimetypes
import mimetypes as mime

# Website Views

def index(request):

	template = "core/index.html"
	context = {}

	return render(request, template, context)

def contact(request):

	template = "core/contact.html"
	context = {}

	return render(request, template, context)

# Authentication Views

def login(request):
	if request.user.is_authenticated():
		messages.info(request, 'You are already logged in.')
		return redirect(reverse('monitor_dashboard'))

	if request.POST:
		user = request.POST.get('user_name')
		pawd = request.POST.get('user_pass')

		user = authenticate(username=user, password=pawd)

		if user is not None:
			if user.is_active:
				login_user(request, user)
				messages.info(request, 'Login successful.')
				if request.GET.get('next'):
					return redirect(request.GET.get('next'))
				else:
					return redirect(reverse('index'))
			else:
				messages.add_message(request, messages.ERROR, 'User account is not active.')
		else:
			messages.add_message(request, messages.ERROR, 'Account not found with those details.')

	context = {}
	template = 'core/login.html'

	return render(request, template, context)

@login_required
def logout(request):
	messages.info(request, 'You have been logged out.')
	logout_user(request)
	return redirect(reverse('index'))

def register(request):
	if request.method == 'POST':
		form = forms.UserCreationForm(request.POST)
		if form.is_valid():
			new_user = form.save()
			return redirect(reverse('login'))
	else:
		form = forms.UserCreationForm()

	return render(request, "core/register.html", {
		'form': form,
	})

def activate(request, code):
	profile = get_object_or_404(models.Profile, activation_code=code)
	if profile:
		profile.user.is_active = True
		profile.date_confirmed = timezone.now()
		profile.activation_code = ''
		profile.save()
		profile.user.save()
		messages.add_message(request, messages.INFO, 'Registration complete, you can login now.')
		return redirect(reverse('login'))

@login_required
def view_profile(request):
	user_profile = models.Profile.objects.get(user=request.user)

	template = 'core/user/profile.html'
	context = {
		'user_profile': user_profile,
	}

	return render(request, template, context)

@login_required
def update_profile(request):
	user_profile = models.Profile.objects.get(user=request.user)
	user_form = forms.UserProfileForm(instance=request.user)
	profile_form = forms.ProfileForm(instance=user_profile)
	if request.method == 'POST':
		user_form = forms.UserProfileForm(request.POST, instance=request.user)
		profile_form = forms.ProfileForm(request.POST, request.FILES, instance=user_profile)
		if profile_form.is_valid() and user_form.is_valid():
			user = user_form.save()
			profile = profile_form.save()
			return redirect(reverse('view_profile'))

	template = 'core/user/update_profile.html'
	context = {
		'profile_form' : profile_form,
		'user_form': user_form,
	}

	return render(request, template, context)

@login_required
def user_home(request):

	task_list = models.Task.objects.filter(assignee=request.user, completed__isnull=True).order_by('due')
	new_task_form = forms.TaskForm()

	template = 'core/user/home.html'
	context = {
		'task_list': task_list,
		'proposals': submission_models.Proposal.objects.filter(status='submission').count(),
		'new_submissions': models.Book.objects.filter(stage__current_stage='submission').count(),
		'in_review': models.Book.objects.filter(stage__current_stage='review').count(),
		'in_editing': models.Book.objects.filter(stage__current_stage='editing').count(),
		'in_production': models.Book.objects.filter(stage__current_stage='production').count(),
		'new_task_form': new_task_form,
		'user_submissions': models.Book.objects.filter(owner=request.user)
	}

	return render(request, template, context)

@login_required
def user_submission(request, submission_id):
	book = get_object_or_404(models.Book, pk=submission_id, owner=request.user)

	template = 'core/user/user_submission.html'
	context = {
		'submission': book,
	}

	return render(request, template, context)

@login_required
def author_contract_signoff(request, submission_id, contract_id):
	contract = get_object_or_404(models.Contract, pk=contract_id)
	submission = get_object_or_404(models.Book, pk=submission_id, owner=request.user, contract=contract)

	if request.POST:
		author_signoff_form = workflow_forms.AuthorContractSignoff(request.POST, request.FILES)
		if author_signoff_form.is_valid():
			author_file = request.FILES.get('author_file')
			new_file = handle_file(author_file, submission, 'contract')
			contract.author_file = new_file
			contract.author_signed_off = timezone.now()
			contract.save()
			return redirect(reverse('user_submission', kwargs={'submission_id': submission_id}))
	else:
		author_signoff_form = workflow_forms.AuthorContractSignoff()

	template = 'core/user/author_contract_signoff.html'
	context = {
		'submission': 'submission',
		'contract': 'contract',
		'author_signoff_form': 'author_signoff_form',
	}

	return render(request, template, context)

@login_required
def reset_password(request):

	if request.method == 'POST':
		password_1 = request.POST.get('password_1')
		password_2 = request.POST.get('password_2')

		if password_1 == password_2:
			if len(password_1) > 8:
				user = User.objects.get(username=request.user.username)
				user.set_password(password_1)
				user.save()
				messages.add_message(request, messages.SUCCESS, 'Password successfully changed.')
				return redirect(reverse('user_home'))
			else:
				messages.add_message(request, messages.ERROR, 'Password is not long enough, must be greater than 8 characters.')
		else:
			messages.add_message(request, messages.ERROR, 'Your passwords do not match.')

	template = 'core/user/reset_password.html'
	context = {}

	return render(request, template, context)

def unauth_reset(request):
	pass

def permission_denied(request):

	template = 'core/403.html'
	context = {}

	return render(request, template, context)


# Dashboard
@login_required
def dashboard(request):

	template = 'core/dashboard/dashboard.html'
	context = {
		'proposals': submission_models.Proposal.objects.exclude(status='declined').exclude(status='accepted'),
		'new_submissions': models.Book.objects.filter(stage__current_stage='submission'),
		'in_review': models.Book.objects.filter(stage__current_stage='review'),
		'in_editing': models.Book.objects.filter(stage__current_stage='editing'),
		'in_production': models.Book.objects.filter(stage__current_stage='production'),
	}

	return render(request, template, context)

# AJAX Handlers

@csrf_exempt
@login_required
def task_complete(request, task_id):

	task = get_object_or_404(models.Task, pk=task_id, assignee=request.user, completed__isnull=True)
	task.completed = timezone.now()
	task.save()
	return HttpResponse('Thanks')

@login_required
def task_new(request):

	new_task_form = forms.TaskForm(request.POST)
	pprint(request.POST)
	if new_task_form.is_valid():
		task = new_task_form.save(commit=False)
		task.creator = request.user
		task.assignee = request.user
		task.save()

		return HttpResponse(json.dumps({'id': task.pk,'text': task.text}))
	else:
		return HttpResponse(new_task_form.errors)

## File helpers
def handle_file(file, book, kind):

	original_filename = str(file._get_name())
	filename = str(uuid4()) + str(os.path.splitext(original_filename)[1])
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

	new_file = models.File(
		mime_type=file_mime,
		original_filename=original_filename,
		uuid_filename=filename,
		stage_uploaded=1,
		kind=kind,
	)
	new_file.save()

	return new_file
