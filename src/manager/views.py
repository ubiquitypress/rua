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
from django.utils.encoding import smart_text

from manager import models
from review import models as review_models
from review import forms as review_f
from manager import forms, logic
from django.conf import settings
from core import models as core_models, forms as core_forms
from core.decorators import is_press_editor
from submission import forms as submission_forms
from submission import models as submission_models

from uuid import uuid4
import os

@is_press_editor
def index(request):
	template = 'manager/index.html'
	context = {}

	return render(request, template, context)

@is_press_editor
def groups(request):

	template = 'manager/groups.html'
	context = {
		'groups': models.Group.objects.all()
	}

	return render(request, template, context)

@is_press_editor
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

@is_press_editor
def group_delete(request, group_id):

	group = get_object_or_404(models.Group, pk=group_id)
	group.delete()

	return redirect('manager_groups')

@is_press_editor
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

@is_press_editor
def group_members_assign(request, group_id, user_id):

	group = get_object_or_404(models.Group, pk=group_id)
	user = get_object_or_404(User, pk=user_id)

	if not models.GroupMembership.objects.filter(user=user, group=group):
		member = models.GroupMembership(user=user, group=group, sequence=9999)
		member.save()
	else:
		messages.add_message(request, messages.WARNING, 'This user is already a member of %s' % group.name)


	return redirect(reverse('manager_group_members', kwargs={'group_id': group.id}))

@is_press_editor
def manager_membership_delete(request, group_id, member_id):

	group = get_object_or_404(models.Group, pk=group_id)
	membership = get_object_or_404(models.GroupMembership, pk=member_id)

	membership.delete()

	return redirect(reverse('manager_group_members', kwargs={'group_id': group.id}))

@is_press_editor
@csrf_exempt
def roles(request):

	template = 'manager/roles.html'
	context = {
		'roles': core_models.Role.objects.all(),
	}

	return render(request, template, context)

@is_press_editor
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

@is_press_editor
def role_action(request, slug, user_id, action):

	user = get_object_or_404(User, pk=user_id)
	role = get_object_or_404(core_models.Role, slug=slug)

	if action == 'add':
		user.profile.roles.add(role)
	elif action == 'remove':
		user.profile.roles.remove(role)

	user.save()

	return redirect(reverse('manager_role', kwargs={'slug': role.slug}))

@is_press_editor
def flush_cache(request):
	cache._cache.flush_all()
	messages.add_message(request, messages.SUCCESS, 'Memcached has been flushed.')

	return redirect(reverse('manager_index'))

@is_press_editor
def settings_index(request):
	
	template = 'manager/settings/index.html'
	context = {
		'settings': [{group.name: core_models.Setting.objects.filter(group=group).order_by('name')} for group in core_models.SettingGroup.objects.all().order_by('name')],
	}

	return render(request, template, context)

@is_press_editor
def edit_setting(request, setting_group, setting_name):
	group = get_object_or_404(core_models.SettingGroup, name=setting_group)
	setting = get_object_or_404(core_models.Setting, group=group, name=setting_name)

	edit_form = forms.EditKey(key_type=setting.types, value=setting.value)

	if request.POST and 'delete' in request.POST:
		setting.value = ''
		setting.save()

		return redirect(reverse('settings_index'))

	if request.POST:
		value = smart_text(request.POST.get('value'))
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

def edit_submission_checklist(request,item_id):
	item = get_object_or_404(submission_models.SubmissionChecklistItem, pk=item_id)
	checkitem_form = submission_forms.CreateSubmissionChecklistItem(instance=item)

	if request.POST:
		checkitem_form = submission_forms.CreateSubmissionChecklistItem(request.POST,instance=item)
		if checkitem_form.is_valid():
			new_check_item = checkitem_form.save()
			return redirect(reverse('submission_checklist'))

	template = 'manager/submission/checklist.html'
	context = {
		'checkitem_form': checkitem_form,
		'editing':True,
		'item':item,
		'checklist_items': submission_models.SubmissionChecklistItem.objects.all()
	}

	return render(request, template, context)

def delete_submission_checklist(request,item_id):
	item = get_object_or_404(submission_models.SubmissionChecklistItem, pk=item_id)
	item.delete()
	
	return redirect(reverse('submission_checklist'))

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

@is_press_editor
def users(request):

	template = 'manager/users/index.html'
	context = {
		'users': User.objects.all(),
		'password': request.GET.get('password', None),
		'username': request.GET.get('username', None),
	}
	return render(request, template, context)

@is_press_editor
def add_user(request):
	user_form = core_forms.FullUserProfileForm()
	profile_form = core_forms.FullProfileForm()

	if request.method == 'POST':
		user_form = core_forms.FullUserProfileForm(request.POST)
		profile_form = core_forms.FullProfileForm(request.POST, request.FILES)
		if profile_form.is_valid() and user_form.is_valid():
			user = user_form.save()

			if 'new_password' in request.POST:
				new_pass = logic.generate_password()
				user.set_password(new_pass)
				messages.add_message(request, messages.SUCCESS, 'New user %s, password set to %s.' % (user.username, new_pass))
				email_text = core_models.Setting.objects.get(group__name='email', name='new_user_email').value
				logic.send_new_user_ack(email_text, user, new_pass)

			user.save()

			profile = profile_form.save(commit=False)
			profile.user = user
			profile.save()

			roles = request.POST.getlist('roles')

			for role in roles:
				role_object = core_models.Role.objects.get(pk=role)
				profile.roles.add(role_object)

			for interest in profile.interest.all():
				profile.interest.remove(interest)

			for interest in request.POST.get('interests').split(','):
				new_interest, c = core_models.Interest.objects.get_or_create(name=interest)
				profile.interest.add(new_interest)

			profile.save()


			return redirect("%s?username=%s&password=%s" % (reverse('manager_users'), user.username, new_pass))

	template = 'manager/users/edit.html'
	context = {
		'profile_form' : profile_form,
		'user_form': user_form,
		'active': 'add',
		'return': request.GET.get('return', False)
	}
	return render(request, template, context)

@is_press_editor
def user_edit(request, user_id):
	user = User.objects.get(pk=user_id)
	user_form = core_forms.UserProfileForm(instance=user)
	profile_form = core_forms.FullProfileForm(instance=user.profile)

	if request.method == 'POST':
		user_form = core_forms.UserProfileForm(request.POST, instance=user)
		profile_form = core_forms.FullProfileForm(request.POST, request.FILES, instance=user.profile)
		if profile_form.is_valid() and user_form.is_valid():
			user = user_form.save()
			profile = profile_form.save()
			for interest in profile.interest.all():
				profile.interest.remove(interest)

			for interest in request.POST.get('interests').split(','):
				new_interest, c = core_models.Interest.objects.get_or_create(name=interest)
				profile.interest.add(new_interest)
			profile.save()
			
			return redirect(reverse('manager_users'))

	template = 'manager/users/edit.html'
	context = {
		'user': user,
		'profile_form' : profile_form,
		'user_form': user_form,
		'active': 'update',
	}
	return render(request, template, context)

@is_press_editor
def inactive_users(request):

	users = User.objects.filter(is_active=False)

	template = 'manager/users/inactive.html'
	context = {
		'users': users,
	}

	return render(request, template, context)

@is_press_editor
def activate_user(request, user_id):

	user = get_object_or_404(models.User, pk=user_id, is_active=False)
	user.is_active = True
	user.save()

	return redirect(reverse('manager_inactive_users'))

@is_press_editor
def key_help(request):
	import json
	with open('%s%s' % (settings.BASE_DIR, '/core/fixtures/key_help.json')) as data_file:    
		data = json.load(data_file)

	template = "manager/keys.html"
	context = {
		'data': data,
		'data_render': json.dumps(data, indent=4)
	}
	return render(request, template, context)

@is_press_editor
def add_new_form(request, form_type):

	if form_type == 'review':
		form = forms.ReviewForm()
	else:
		form = forms.ProposalForms()

	if request.POST:
		if form_type == 'review':
			form = forms.ReviewForm(request.POST)
		else:
			form = forms.ProposalForms(request.POST)

		if form.is_valid:
			form.save()

		return redirect(reverse('manager_%s_forms' % form_type))

	template = 'manager/add_new_form.html'
	context = {
		'form': form,
		'form_type': form_type,
	}
	return render(request, template, context)

@is_press_editor
def proposal_forms(request):

	template = 'manager/proposal/forms.html'
	context = {
		'proposal_forms': core_models.ProposalForm.objects.all()
	}
	return render(request, template, context)

@is_press_editor
def edit_proposal_form(request, form_id, relation_id=None):

	form = get_object_or_404(core_models.ProposalForm, pk=form_id)

	if relation_id:
		relation = get_object_or_404(core_models.ProposalFormElementsRelationship, pk=relation_id)
		element_form = forms.ProposalElement(instance=relation.element)
		relation_form = forms.ProposalElementRelationship(instance=relation)
	else:
		element_form = forms.ProposalElement()
		relation_form = forms.ProposalElementRelationship()

	if request.POST:
		if relation_id:
			element_form = forms.ProposalElement(request.POST, instance=relation.element)
			relation_form = forms.ProposalElementRelationship(request.POST, instance=relation)
		else:
			element_form = forms.ProposalElement(request.POST)
			relation_form = forms.ProposalElementRelationship(request.POST)

		if element_form.is_valid() and relation_form.is_valid():
			new_element = element_form.save()

			new_relation = relation_form.save(commit=False)
			new_relation.form = form
			new_relation.element = new_element
			new_relation.save()

			form.proposal_fields.add(new_relation)

			return redirect(reverse('manager_edit_proposal_form', kwargs={'form_id': form_id}))

	template = 'manager/proposal/edit_form.html'
	context = {
		'form': form,
		'element_form': element_form,
		'relation_form': relation_form,
	}
	return render(request, template, context)

@is_press_editor
def preview_proposal_form(request, form_id):

	form = get_object_or_404(core_models.ProposalForm, pk=form_id)

	preview_form = forms.GeneratedForm(form=core_models.ProposalForm.objects.get(pk=form_id))
	fields = core_models.ProposalFormElementsRelationship.objects.filter(form=form)
	default_fields = forms.DefaultForm()

	template = 'manager/proposal/preview_form.html'
	context = {
		'form': form,
		'preview_form': preview_form,
		'fields': fields,
		'default_fields': default_fields,
	}
	return render(request, template, context)

@is_press_editor
def delete_proposal_form_element(request, form_id, relation_id):

	form = get_object_or_404(core_models.ProposalForm, pk=form_id)
	relation = get_object_or_404(core_models.ProposalFormElementsRelationship, pk=relation_id)

	relation.element.delete()
	relation.delete()

	return redirect(reverse('manager_edit_proposal_form', kwargs={'form_id': form_id}))

@is_press_editor
def review_forms(request):

	template = 'manager/review/forms.html'
	context = {
		'review_forms': review_models.Form.objects.all()
	}
	return render(request, template, context)

@is_press_editor
def edit_review_form(request, form_id, relation_id=None):

	form = get_object_or_404(review_models.Form, pk=form_id)

	if relation_id:
		relation = get_object_or_404(review_models.FormElementsRelationship, pk=relation_id)
		element_form = forms.FormElement(instance=relation.element)
		relation_form = forms.FormElementsRelationship(instance=relation)
	else:
		element_form = forms.ProposalElement()
		relation_form = forms.FormElementsRelationship()

	if request.POST:
		if relation_id:
			element_form = forms.FormElement(request.POST, instance=relation.element)
			relation_form = forms.FormElementsRelationship(request.POST, instance=relation)
		else:
			element_form = forms.FormElement(request.POST)
			relation_form = forms.FormElementsRelationship(request.POST)

		if element_form.is_valid() and relation_form.is_valid():
			new_element = element_form.save()

			new_relation = relation_form.save(commit=False)
			new_relation.form = form
			new_relation.element = new_element
			new_relation.save()

			form.form_fields.add(new_relation)

			return redirect(reverse('manager_edit_review_form', kwargs={'form_id': form_id}))

	template = 'manager/review/edit_form.html'
	context = {
		'form': form,
		'element_form': element_form,
		'relation_form': relation_form,
	}
	return render(request, template, context)

@is_press_editor
def preview_review_form(request, form_id):

	form = get_object_or_404(review_models.Form, pk=form_id)

	preview_form = forms.GeneratedReviewForm(form=review_models.Form.objects.get(pk=form_id))
	fields = review_models.FormElementsRelationship.objects.filter(form=form)

	template = 'manager/review/preview_form.html'
	context = {
		'form': form,
		'preview_form': preview_form,
		'fields': fields,
	}
	return render(request, template, context)

@is_press_editor
def delete_review_form_element(request, form_id, relation_id):

	form = get_object_or_404(review_models.Form, pk=form_id)
	relation = get_object_or_404(review_models.FormElementsRelationship, pk=relation_id)

	relation.element.delete()
	relation.delete()

	return redirect(reverse('manager_edit_review_form', kwargs={'form_id': form_id}))


## File handler

@is_press_editor
def handle_file(request, file):

	original_filename = str(file._get_name())
	filename = str(uuid4()) + '.' + str(os.path.splitext(original_filename)[1])
	folder_structure = os.path.join(settings.BASE_DIR, 'media', 'settings')

	if not os.path.exists(folder_structure):
		os.makedirs(folder_structure)

	path = os.path.join(folder_structure, str(filename))
	fd = open(path, 'wb')
	for chunk in file.chunks():
		fd.write(chunk)
	fd.close()

	return filename


## AJAX Handler

@is_press_editor
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

@is_press_editor
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
	
@is_press_editor
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
