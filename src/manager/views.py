from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib import messages

from manager import models
from manager import forms
from core import models as core_models

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


def role_action(request, slug, user_id, action):

	user = get_object_or_404(User, pk=user_id)
	role = get_object_or_404(core_models.Role, slug=slug)

	if action == 'add':
		user.profile.roles.add(role)
	elif action == 'remove':
		user.profile.roles.remove(role)

	user.save()

	return redirect(reverse('manager_role', kwargs={'slug': role.slug}))


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
