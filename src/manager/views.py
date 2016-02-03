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
def proposal_forms(request):

	proposal_forms = core_models.ProposalForm.objects.all()
	choices_form = forms.ProposalForm()
	selected_form = core_models.Setting.objects.get(name='proposal_form').value
	if request.POST:
		choices_form = forms.ProposalForm(request.POST)
		if choices_form.is_valid:
			setting = core_models.Setting.objects.get(name='proposal_form')
			setting.value = int(request.POST.get('selection'))
			setting.save()
			messages.add_message(request, messages.INFO, 'Proposal succesfully changed')
			return redirect(reverse('proposal_forms'))

	template = 'manager/proposal/proposal_forms.html'


	context = {
		'forms':proposal_forms,
		'choices_form':choices_form,
		'selected_form':int(selected_form),
	}

	return render(request, template, context)

@is_press_editor
def view_proposal_form(request,form_id):

	form = core_models.ProposalForm.objects.get(id=form_id)

	try:
		preview_form = forms.GeneratedForm(form=core_models.ProposalForm.objects.get(pk=form_id))
	except (ObjectDoesNotExist, ValueError):
		preview_form = None

	fields = core_models.ProposalFormElementsRelationship.objects.filter(form=form)
	if request.POST and "delete" in request.POST:
		index = int(request.POST.get("delete"))
		field = fields[index]
		field.delete()
		return redirect(reverse('manager_view_proposal_form',kwargs={'form_id': form_id}))
	
	default_fields = forms.DefaultForm()
	template = 'manager/proposal/view_form.html'

	context = {
		'form': form,
		'fields':fields,
		'preview_form' : preview_form,
		'default_fields' : default_fields,
	}

	return render(request, template, context)

@is_press_editor
def proposal_form_elements(request):

	elements = core_models.ProposalFormElement.objects.all()

	new_form = forms.StagesProposalFormElementForm()

	if request.POST and "delete" in request.POST:
		index = int(request.POST.get("delete"))
		field = elements[index]
		field.delete()
		return redirect(reverse('manager_proposal_form_elements'))
	elif request.POST:
		form_element_form=forms.StagesProposalFormElementForm(request.POST)
		if form_element_form.is_valid():
			form_element_form.save()
			return redirect(reverse('manager_proposal_form_elements'))


	template = 'manager/proposal/elements.html'

	context = {
		'elements': elements,
		'new_form':new_form
	}

	return render(request, template, context)

@is_press_editor
def add_proposal_field(request,form_id):

	form = core_models.ProposalForm.objects.get(id=form_id)
	fields = core_models.ProposalFormElementsRelationship.objects.filter(form=form)
	elements = core_models.ProposalFormElement.objects.all()
	try:
		preview_form = forms.GeneratedForm(form=form)
	except (ObjectDoesNotExist, ValueError):
		preview_form = None
	default_fields = forms.DefaultForm()
	new_form = forms.StagesProposalFormElementRelationshipForm()
	if request.POST and 'finish' in request.POST:
		print 'Finish'
		return redirect(reverse('manager_view_proposal_form',kwargs={'form_id': form_id}))
	elif request.POST and "delete" in request.POST:
		index = int(request.POST.get("delete"))
		field = fields[index]
		field.delete()
		return redirect(reverse('manager_add_proposal_form_field',kwargs={'form_id': form_id}))
	elif request.POST:
		field_form = forms.StagesProposalFormElementRelationshipForm(request.POST)
		width = request.POST.get("width")
		element_index = request.POST.get("element")
		help_text = request.POST.get("help_text")
		order = int(request.POST.get("order"))

		element_id = int(element_index)
		element = core_models.ProposalFormElement.objects.get(pk=element_id)
		print element.name
		relationship=core_models.ProposalFormElementsRelationship(form=form,element=element,width=width,order=order,help_text=help_text)
		relationship.save()
		fields = core_models.ProposalFormElementsRelationship.objects.filter(form=form)
		form.form_fields=fields
		form.save()
		return redirect(reverse('manager_add_proposal_form_field',kwargs={'form_id': form_id}))
	template = 'manager/proposal/add_field.html'

	context = {
		'form': form,
		'new_form':new_form,
		'fields': fields,
		'preview_form':preview_form,
		'default_fields':default_fields,
	}

	return render(request, template, context)

@is_press_editor
def edit_proposal_field(request,form_id,field_id):

	form = core_models.ProposalForm.objects.get(id=form_id)
	fields = core_models.ProposalFormElementsRelationship.objects.filter(form=form)
	current_field = core_models.ProposalFormElementsRelationship.objects.get(pk=field_id)
	elements = core_models.ProposalFormElement.objects.all()
	
	try:
		preview_form = forms.GeneratedForm(form=form)
	except (ObjectDoesNotExist, ValueError):
		preview_form = None

	default_fields = forms.DefaultForm()
	new_form = forms.StagesProposalFormElementRelationshipForm(instance=current_field)
	if request.POST and 'finish' in request.POST:
		print 'Finish'
		return redirect(reverse('manager_view_proposal_form',kwargs={'form_id': form_id}))
	elif request.POST and "delete" in request.POST:
		index = int(request.POST.get("delete"))
		field = fields[index]
		field.delete()
		return redirect(reverse('manager_add_proposal_form_field',kwargs={'form_id': form_id}))
	elif request.POST:
		field_form = forms.StagesProposalFormElementRelationshipForm(request.POST,instance=current_field)

		width = request.POST.get("width")
		element_index = request.POST.get("element")
		help_text = request.POST.get("help_text")
		order = int(request.POST.get("order"))
		index = int(element_index)-1
		element_id = elements[int(element_index)-1].pk
		element = core_models.ProposalFormElement.objects.get(pk=element_id)

		current_field.element = element
		current_field.width = width
		current_field.help_text = help_text
		current_field.order = order
		current_field.save()

		fields = core_models.ProposalFormElementsRelationship.objects.filter(form=form)
		form.form_fields=fields
		form.save()
		return redirect(reverse('manager_add_proposal_form_field',kwargs={'form_id': form_id}))
	
	template = 'manager/proposal/add_field.html'

	context = {
		'form': form,
		'new_form':new_form,
		'fields': fields,
		'current_field':current_field,
		'update':True,
		'preview_form':preview_form,
		'default_fields':default_fields,
	}

	return render(request, template, context)

@is_press_editor
def add_proposal_form(request, form_id = None):
	edit = True
	if form_id:
		proposal = core_models.ProposalForm.objects.get(id=form_id)
		form = forms.StagesProposalForm(instance = proposal)
	else: 
		edit = False
		proposal = None
		form = forms.StagesProposalForm()

	if request.POST:
		if form_id:
			proposal_form = forms.StagesProposalForm(request.POST, instance = proposal)
		else:
			proposal_form = forms.StagesProposalForm(request.POST)

		if proposal_form.is_valid():
			if form_id:
				new_form = proposal_form.save(commit = False)
				proposal.name = request.POST.get("name")
				proposal.ref = request.POST.get("ref")
				proposal.intro_text = request.POST.get("intro_text")
				proposal.completion_text = request.POST.get("completion_text")
				proposal.save()
				return redirect(reverse('manager_view_proposal_form',kwargs={'form_id': form_id}))
			else:
				new_form = proposal_form.save()
				return redirect(reverse('manager_create_proposal_elements',kwargs={'form_id': new_form.id}))
	
		else:
			print form.errors
	template = 'manager/proposal/add_form.html'

	context = {
		'new_form': form,
		'proposal': proposal,
		'edit' : edit,

	}

	return render(request, template, context)

@is_press_editor
def create_proposal_elements(request,form_id):

	form = core_models.ProposalForm.objects.get(id=form_id)
	elements = core_models.ProposalFormElement.objects.all()
	new_form = forms.StagesProposalFormElementForm()

	if request.POST and "delete" in request.POST:
		index = int(request.POST.get("delete"))
		field = elements[index]
		field.delete()
		return redirect(reverse('manager_create_proposal_elements',kwargs={'form_id': form_id}))
	elif request.POST and 'continue' in request.POST:
		form_element_form=forms.StagesProposalFormElementForm(request.POST)
		if form_element_form.is_valid():
			form_element_form.save()
		return redirect(reverse('manager_add_proposal_form_field',kwargs={'form_id': form_id}))
	elif request.POST:
		form_element_form=forms.StagesProposalFormElementForm(request.POST)
		if form_element_form.is_valid():
			form_element_form.save()
			return redirect(reverse('manager_create_proposal_elements',kwargs={'form_id': form_id}))

	template = 'manager/proposal/create_elements.html'
	context = {
		'form': form,
		'new_form':new_form,
		'elements' : elements,
	}
	return render(request, template, context)
@is_press_editor
def edit_proposal_element(request,form_id,element_id):

	form = core_models.ProposalForm.objects.get(id=form_id)
	elements = core_models.ProposalFormElement.objects.all()
	current_element = core_models.ProposalFormElement.objects.get(pk=element_id)
	new_form = forms.StagesProposalFormElementForm(instance=current_element)

	if request.POST and "delete" in request.POST:
		index = int(request.POST.get("delete"))
		field = elements[index]
		field.delete()
		return redirect(reverse('manager_create_proposal_elements',kwargs={'form_id': form_id}))
	elif request.POST and 'continue' in request.POST:
		form_element_form=forms.StagesProposalFormElementForm(request.POST,instance=current_element)
		if form_element_form.is_valid():
			form_element_form.save()
		return redirect(reverse('manager_add_proposal_form_field',kwargs={'form_id': form_id}))
	elif request.POST and 'update' in request.POST:
		form_element_form=forms.StagesProposalFormElementForm(request.POST,instance=current_element)
		if form_element_form.is_valid():
			new_element=form_element_form.save(commit=False)
			current_element.name = new_element.name
			current_element.choices = new_element.choices
			current_element.field_type = new_element.field_type
			current_element.required = new_element.required
			current_element.save()
		return redirect(reverse('manager_create_proposal_elements',kwargs={'form_id': form_id}))

	template = 'manager/proposal/create_elements.html'
	context = {
		'form': form,
		'new_form':new_form,
		'elements' : elements,
		'update':True,
		'element':current_element,
	}
	return render(request, template, context)
@is_press_editor
def review_forms(request):

	forms = review_models.Form.objects.all()

	template = 'manager/review/review_forms.html'
	context = {
		'forms': forms,
	}
	return render(request, template, context)

@is_press_editor
def view_review_form(request,form_id):

	form = review_models.Form.objects.get(id=form_id)
	fields = review_models.FormElementsRelationship.objects.filter(form=form)
	try:
		preview_form = review_f.GeneratedForm(form=form)
	except (ObjectDoesNotExist, ValueError):
		preview_form = None

	if request.POST and "delete" in request.POST:
		index = int(request.POST.get("delete"))
		field = fields[index]
		field.delete()
		return redirect(reverse('manager_view_review_form',kwargs={'form_id': form_id}))

	template = 'manager/review/view_form.html'
	context = {
		'form': form,
		'preview_form':preview_form,
		'fields':fields,
	}
	return render(request, template, context)

@is_press_editor
def review_form_elements(request):

	elements = review_models.FormElement.objects.all()

	new_form = forms.FormElementForm()

	if request.POST and "delete" in request.POST:
		index = int(request.POST.get("delete"))
		field = elements[index]
		field.delete()
		return redirect(reverse('manager_review_form_elements'))
	elif request.POST:
		form_element_form=forms.FormElementForm(request.POST)
		if form_element_form.is_valid():
			form_element_form.save()
			return redirect(reverse('manager_review_form_elements'))


	template = 'manager/review/elements.html'
	context = {
		'elements': elements,
		'new_form':new_form
	}
	return render(request, template, context)

@is_press_editor
def add_field(request,form_id):

	form = review_models.Form.objects.get(id=form_id)
	fields = review_models.FormElementsRelationship.objects.filter(form=form)
	elements = review_models.FormElement.objects.all().order_by('pk')
	new_form = forms.FormElementsRelationshipForm()

	form = review_models.Form.objects.get(id=form_id)
	fields = review_models.FormElementsRelationship.objects.filter(form=form)

	try:
		preview_form = review_f.GeneratedForm(form=form)
	except (ObjectDoesNotExist, ValueError):
		preview_form = None


	if request.POST and 'finish' in request.POST:
		return redirect(reverse('manager_view_review_form',kwargs={'form_id': form_id}))
	elif request.POST and "delete" in request.POST:
		index = int(request.POST.get("delete"))
		field = fields[index]
		field.delete()
		return redirect(reverse('manager_add_review_form_field',kwargs={'form_id': form_id}))
	elif request.POST:
		field_form = forms.FormElementsRelationshipForm(request.POST)
		width = request.POST.get("width")
		element_index = request.POST.get("element")
		help_text = request.POST.get("help_text")
		order = int(request.POST.get("order"))
		element_id = int(element_index)
		element = review_models.FormElement.objects.get(pk=element_id)
		relationship=review_models.FormElementsRelationship(form=form,element=element,width=width,order=order,help_text=help_text)
		relationship.save()
		fields = review_models.FormElementsRelationship.objects.filter(form=form)
		form.form_fields=fields
		form.save()
		return redirect(reverse('manager_add_review_form_field',kwargs={'form_id': form_id}))
	
	template = 'manager/review/add_field.html'
	context = {
		'form': form,
		'new_form':new_form,
		'fields': fields,
		'preview_form':preview_form,
	}
	return render(request, template, context)


@is_press_editor
def edit_elements(request, form_id, element_id):

	form =  review_models.Form.objects.get(id=form_id)
	elements = review_models.FormElement.objects.all()
	current_element = get_object_or_404(review_models.FormElement, pk = element_id)

	new_form = forms.FormElementForm(instance=current_element)
	if request.POST and "delete" in request.POST:
		index = int(request.POST.get("delete"))
		field = elements[index]
		field.delete()
		return redirect(reverse('manager_create_elements',kwargs={'form_id': form_id}))
	elif request.POST and 'continue' in request.POST:
		form_element_form=forms.FormElementForm(request.POST, instance = current_element)
		if form_element_form.is_valid():
			new_element = form_element_form.save(commit=False)

		return redirect(reverse('manager_add_review_form_field',kwargs={'form_id': form_id}))
	elif request.POST:
		form_element_form=forms.FormElementForm(request.POST, instance = current_element)
		if form_element_form.is_valid():
			new_element = form_element_form.save(commit=False)
			current_element.name = new_element.name
			current_element.choices = new_element.choices
			current_element.field_type = new_element.field_type
			current_element.required = new_element.required
			current_element.save()
			return redirect(reverse('manager_create_elements',kwargs={'form_id': form_id}))

	template = 'manager/review/create_elements.html'
	context = {
		'form': form,
		'new_form':new_form,
		'elements' : elements,
		'current_element':current_element,
		'edit': True,
	}
	return render(request, template, context)


@is_press_editor
def edit_field(request,form_id, field_id):

	form = review_models.Form.objects.get(id=form_id)
	fields = review_models.FormElementsRelationship.objects.filter(form=form)
	current_field = get_object_or_404(review_models.FormElementsRelationship, pk=field_id)

	elements = review_models.FormElement.objects.all().order_by('pk')
	new_form = forms.FormElementsRelationshipForm(instance = current_field)

	form = review_models.Form.objects.get(id=form_id)
	fields = review_models.FormElementsRelationship.objects.filter(form=form)

	try:
		preview_form = review_f.GeneratedForm(form=form)
	except (ObjectDoesNotExist, ValueError):
		preview_form = None


	if request.POST and 'finish' in request.POST:
		return redirect(reverse('manager_view_review_form',kwargs={'form_id': form_id}))
	elif request.POST and "delete" in request.POST:
		index = int(request.POST.get("delete"))
		field = fields[index]
		field.delete()
		return redirect(reverse('manager_add_review_form_field',kwargs={'form_id': form_id}))
	elif request.POST:

		field_form = forms.FormElementsRelationshipForm(request.POST, instance=current_field)

		width = request.POST.get("width")
		element_index = request.POST.get("element")
		help_text = request.POST.get("help_text")
		order = int(request.POST.get("order"))
		index = int(element_index)-1
		element_id = elements[int(element_index)-1].pk
		element = review_models.FormElement.objects.get(pk=element_id)

		current_field.element = element
		current_field.width = width
		current_field.help_text = help_text
		current_field.order = order
		current_field.save()

		fields = review_models.FormElementsRelationship.objects.filter(form=form)
		form.form_fields=fields
		form.save()
		
		return redirect(reverse('manager_add_review_form_field',kwargs={'form_id': form_id}))
	
	template = 'manager/review/add_field.html'
	context = {
		'form': form,
		'new_form':new_form,
		'fields': fields,
		'preview_form':preview_form,
		'current_field':current_field,
	}
	return render(request, template, context)

@is_press_editor
def add_form(request, form_id = None):
	edit = True
	if form_id:
		review =  review_models.Form.objects.get(id=form_id)
		form  = forms.ReviewForm(instance = review)
	else:
		edit = False
		review = None
		form = forms.ReviewForm()

	if request.POST:
		if form_id:
			review_form = forms.ReviewForm(request.POST, instance = review)
		else:
			review_form = forms.ReviewForm(request.POST)

		if review_form.is_valid():
			if form_id:
				new_form = review_form.save(commit=False)
				review.name = request.POST.get("name")
				review.ref = request.POST.get("ref")
				review.intro_text = request.POST.get("intro_text")
				review.completion_text = request.POST.get("completion_text")
				review.save()
				return redirect(reverse('manager_view_review_form',kwargs={'form_id': form_id}))
			else:
				new_form = review_form.save()
				return redirect(reverse('manager_create_elements',kwargs={'form_id': new_form.id}))

	
		else:
			print form.errors

	template = 'manager/review/add_form.html'
	context = {
		'new_form': form,
		'review': review,
		'edit' : edit,
	}
	return render(request, template, context)

@is_press_editor
def create_elements(request,form_id):

	form =  review_models.Form.objects.get(id=form_id)
	elements = review_models.FormElement.objects.all()
	new_form = forms.FormElementForm()
	if request.POST and "delete" in request.POST:
		index = int(request.POST.get("delete"))
		field = elements[index]
		field.delete()
		return redirect(reverse('manager_create_elements',kwargs={'form_id': form_id}))
	elif request.POST and 'continue' in request.POST:
		form_element_form=forms.FormElementForm(request.POST)
		if form_element_form.is_valid():
			form_element_form.save()
		return redirect(reverse('manager_add_review_form_field',kwargs={'form_id': form_id}))
	elif request.POST:
		form_element_form=forms.FormElementForm(request.POST)
		if form_element_form.is_valid():
			form_element_form.save()
			return redirect(reverse('manager_create_elements',kwargs={'form_id': form_id}))

	template = 'manager/review/create_elements.html'
	context = {
		'form': form,
		'new_form':new_form,
		'elements' : elements,
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

	users = User.objects.filter(active=False)

	template = 'manager/users/inactive.html'
	context = {
		'users': users,
	}


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
