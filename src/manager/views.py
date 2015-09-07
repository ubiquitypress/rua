from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist

from manager import models
from manager import forms
from django.conf import settings
from core import models as core_models
from submission import forms as submission_forms
from submission import models as submission_models

from uuid import uuid4
import os

@staff_member_required
def index(request):

	template = 'manager/index.html'
	context = {}

	return render(request, template, context)

@staff_member_required
def groups(request):

	template = 'manager/groups.html'
	context = {
		'groups': models.Group.objects.all()
	}

	return render(request, template, context)

@staff_member_required
def group(request, group_id=None):

	form = forms.GroupForm()

	if group_id:
		group = get_object_or_404(models.Group, pk=group_id)
		form = forms.GroupForm(instance=group)
	else:
		group = None

	if request.method == 'POST':
		if group_id:
			form = forms.GroupForm(request.POST, instance=group)
		else:
			form = forms.GroupForm(request.POST)

		if form.is_valid():
			form.save()
			return redirect('manager_groups')

	template = 'manager/group.html'
	context = {
		'form': form,
		'group': group,
	}

	return render(request, template, context)

@staff_member_required
def group_delete(request, group_id):

	group = get_object_or_404(models.Group, pk=group_id)
	group.delete()

	return redirect('manager_groups')

@staff_member_required
def group_members(request, group_id):

	group = get_object_or_404(models.Group, pk=group_id)
	members = models.GroupMembership.objects.filter(group=group)
	users = User.objects.all().order_by('last_name')

	template = 'manager/members.html'
	context = {
		'group': group,
		'members': members,
		'users': users,
	}

	return render(request, template, context)

@staff_member_required
def group_members_assign(request, group_id, user_id):

	group = get_object_or_404(models.Group, pk=group_id)
	user = get_object_or_404(User, pk=user_id)

	if not models.GroupMembership.objects.filter(user=user, group=group):
		member = models.GroupMembership(user=user, group=group, sequence=9999)
		member.save()
	else:
		messages.add_message(request, messages.WARNING, 'This user is already a member of %s' % group.name)


	return redirect(reverse('manager_group_members', kwargs={'group_id': group.id}))

@staff_member_required
def manager_membership_delete(request, group_id, member_id):

	group = get_object_or_404(models.Group, pk=group_id)
	membership = get_object_or_404(models.GroupMembership, pk=member_id)

	membership.delete()

	return redirect(reverse('manager_group_members', kwargs={'group_id': group.id}))

@staff_member_required
def roles(request):

	template = 'manager/roles.html'
	context = {
		'roles': core_models.Role.objects.all(),
	}

	return render(request, template, context)

@staff_member_required
def role(request, slug):

	role = get_object_or_404(core_models.Role, slug=slug)
	users_with_role = User.objects.filter(profile__roles__slug=slug)
	users = User.objects.all().order_by('last_name').exclude(profile__roles__slug=slug)

	template = 'manager/role.html'
	context = {
		'role': role,
		'users': users,
		'users_with_role': users_with_role,
	}

	return render(request, template, context)

@staff_member_required
def role_action(request, slug, user_id, action):

	user = get_object_or_404(User, pk=user_id)
	role = get_object_or_404(core_models.Role, slug=slug)

	if action == 'add':
		user.profile.roles.add(role)
	elif action == 'remove':
		user.profile.roles.remove(role)

	user.save()

	return redirect(reverse('manager_role', kwargs={'slug': role.slug}))

@staff_member_required
def flush_cache(request):
	cache._cache.flush_all()
	messages.add_message(request, messages.SUCCESS, 'Memcached has been flushed.')

	return redirect(reverse('manager_index'))

@staff_member_required
def settings_index(request):
	
	template = 'manager/settings/index.html'
	context = {
		'settings': [{group.name: core_models.Setting.objects.filter(group=group).order_by('name')} for group in core_models.SettingGroup.objects.all().order_by('name')],
	}

	return render(request, template, context)

@staff_member_required
def edit_setting(request, setting_group, setting_name):
	group = get_object_or_404(core_models.SettingGroup, name=setting_group)
	setting = get_object_or_404(core_models.Setting, group=group, name=setting_name)

	edit_form = forms.EditKey(key_type=setting.types, value=setting.value)

	if request.POST and 'delete' in request.POST:
		setting.value = ''
		setting.save()

		return redirect(reverse('settings_index'))

	if request.POST:
		value = request.POST.get('value')
		if request.FILES:
			value = handle_file(request, request.FILES['value'])

		setting.value = value
		setting.save()

		cache._cache.flush_all()

		return redirect(reverse('settings_index'))


	template = 'manager/settings/edit_setting.html'
	context = {
		'setting': setting,
		'group': group,
		'edit_form': edit_form,
	}

	return render(request, template, context)

def submission_checklist(request):

	checkitem_form = submission_forms.CreateSubmissionChecklistItem()

	if request.POST:
		checkitem_form = submission_forms.CreateSubmissionChecklistItem(request.POST)
		if checkitem_form.is_valid():
			new_check_item = checkitem_form.save()
			return redirect(reverse('submission_checklist'))

	template = 'manager/submission/checklist.html'
	context = {
		'checkitem_form': checkitem_form,
		'checklist_items': submission_models.SubmissionChecklistItem.objects.all()
	}

	return render(request, template, context)

@staff_member_required
def proposal_forms(request):
	try:
		selected_form_id = core_models.Setting.objects.get(name='proposal_form').value
		selected_form = forms.GeneratedForm(form=core_models.ProposalForm.objects.get(pk=selected_form_id))
	except (ObjectDoesNotExist, ValueError):
		selected_form_id = None
		selected_form = None
	
	choices_form = forms.ProposalForm()
	default_fields = forms.DefaultForm()

	if request.POST:
		choices_form = forms.ProposalForm(request.POST)
		if choices_form.is_valid:
			setting = core_models.Setting.objects.get(name='proposal_form')
			setting.value = int(request.POST.get('selection'))
			setting.save()
			messages.add_message(request, messages.INFO, 'Proposal succesfully changed')
			return redirect(reverse('proposal_forms'))

	template = 'manager/submission/proposal_forms.html'

	context = {
		'choices_form': choices_form,
		'selected_form' : selected_form,
		'default_fields': default_fields,
	}

	return render(request, template, context)


## File handler

@staff_member_required
def handle_file(request, file):

	original_filename = str(file._get_name())
	filename = str(uuid4()) + '.' + str(os.path.splitext(original_filename)[1])
	folder_structure = os.path.join(settings.BASE_DIR, 'files', 'settings')

	if not os.path.exists(folder_structure):
		os.makedirs(folder_structure)

	path = os.path.join(folder_structure, str(filename))
	fd = open(path, 'wb')
	for chunk in file.chunks():
		fd.write(chunk)
	fd.close()

	return filename


## AJAX Handler

@staff_member_required
@csrf_exempt
def groups_order(request):

	groups = models.Group.objects.all()

	if request.POST:
		ids = request.POST.getlist('%s[]' % 'group')
		ids = [int(_id) for _id in ids]
		for group in groups:
			# Get the index:
			group.sequence = ids.index(group.id)
			group.save()

		response = 'Thanks'

	else:
		response = 'Nothing to process, post required'

	return HttpResponse(response)

@staff_member_required
@csrf_exempt
def group_members_order(request, group_id):

	group = get_object_or_404(models.Group, pk=group_id)
	memberships = models.GroupMembership.objects.filter(group=group)

	if request.POST:
		ids = request.POST.getlist('%s[]' % 'member')
		ids = [int(_id) for _id in ids]
		for membership in memberships:
			# Get the index:
			membership.sequence = ids.index(membership.id)
			membership.save()

		response = 'Thanks'

	else:
		response = 'Nothing to process, post required'

	return HttpResponse(response)

@staff_member_required
@csrf_exempt
def checklist_order(request):

	checklist_items = submission_models.SubmissionChecklistItem.objects.all()

	if request.POST:
		ids = request.POST.getlist('%s[]' % 'check')
		ids = [int(_id) for _id in ids]

		for item in checklist_items:
			item.sequence = ids.index(item.id)
			item.save()

		response = 'Thanks'
	else:
		response = 'Nothing to process, POST required.'

	return HttpResponse(response)
