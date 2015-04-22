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

from core import models
from core import forms

from pprint import pprint

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

	template = 'core/user/home.html'
	context = {
		'task_list': task_list,
		'new_submissions': models.Book.objects.filter(stage__current_stage='submission').count(),
		'in_review': models.Book.objects.filter(Q(stage__current_stage='i_review') | Q(stage__current_stage='e_review')).count(),
		'in_editing': models.Book.objects.filter(Q(stage__current_stage='copy_editing') | Q(stage__current_stage='indexing')).count(),
		'in_production': models.Book.objects.filter(stage__current_stage='production').count()
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


# AJAX Handlers

@csrf_exempt
@login_required
def task_complete(request, task_id):

	task = get_object_or_404(models.Task, pk=task_id, assignee=request.user, completed__isnull=True)
	task.completed = timezone.now()
	task.save()
	return HttpResponse('Thanks')
