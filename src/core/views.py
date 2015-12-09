from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import logout as logout_user
from django.contrib.auth import login as login_user
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse, StreamingHttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core import serializers
from django.conf import settings
from  __builtin__ import any as string_any

from core import log, models, forms, logic
from email import send_email
from files import handle_file_update,handle_attachment,handle_file
from submission import models as submission_models
from core.decorators import is_editor, is_book_editor, is_book_editor_or_author, is_onetasker,is_author
from review import forms as review_forms

from pprint import pprint
import json
from time import strftime
import time
from uuid import uuid4
from manager import models as manager_models
from submission import forms as submission_forms
from django.db import IntegrityError
import os
import mimetypes
import mimetypes as mime

# Website Views

def index(request):
	return redirect(reverse('login'))

def contact(request):

	template = "core/contact.html"
	context = {}

	return render(request, template, context)

# Authentication Views
def dashboard(request):
	if request.user.is_authenticated():
		roles=  request.user.profile.roles.all()
		if request.GET.get('next'):
			return redirect(request.GET.get('next'))
		elif string_any('Editor' in role.name for role in roles):
			return redirect(reverse('editor_dashboard'))
		elif string_any('Author' in role.name for role in roles):
			return redirect(reverse('author_dashboard'))
		elif string_any('Reviewer' in role.name for role in roles):
			return redirect(reverse('reviewer_dashboard'))
		else:
			return redirect(reverse('onetasker_dashboard'))
			
def login(request):
	if request.user.is_authenticated():
		messages.info(request, 'You are already logged in.')
		roles=  request.user.profile.roles.all()
		if request.GET.get('next'):
			return redirect(request.GET.get('next'))
		else:
			return redirect(reverse('user_dashboard'))
			

	if request.POST:
		user = request.POST.get('user_name')
		pawd = request.POST.get('user_pass')

		user = authenticate(username=user, password=pawd)

		if user is not None:
			if user.is_active:
				login_user(request, user)
				messages.info(request, 'Login successful.')
				roles=  user.profile.roles.all()
				if request.GET.get('next'):
					return redirect(request.GET.get('next'))
				else:
					return redirect(reverse('user_dashboard'))
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
	try:
		user_profile = models.Profile.objects.get(user=request.user)
	except:
		user_profile = models.Profile(user=request.user)
		user_profile.save()
 	name_len=len(request.user.first_name)+len(request.user.last_name)
 	print name_len

	template = 'core/user/profile.html'
	context = {
		'user_profile': user_profile,
		'name_width':name_len*9,
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

def oai(request):
	try:
		base_url = models.Setting.objects.get(group__name='general', name='base_url').value
	except:
		base_url='localhost:8000'
	oai_dc = 'http://%s/oai' % (base_url)
	oai_identifier = models.Setting.objects.get(group__name='general', name='oai_identifier').value

	books = models.Book.objects.all()
	list_of_books =[[{}] for t in range(0,len(books)) ]	
	t=0
	for book in books:
		try:
			isbns = models.Identifier.objects.filter(book=book).exclude(identifier='pub_id').exclude(identifier='urn').exclude(identifier='doi')
		except:
			isbns=None
		formats=book.formats()
		list_format=[]
		for format in formats:
			list_format.append(format.file.mime_type)
		list_of_books[t] = [{'book': book, 'isbns': isbns,'formats':list_format,}]
		t=t+1  
	template = 'core/oai.xml'
	context = {
		'books': list_of_books,
		'oai_dc': oai_dc,
		'base_url':base_url,
		'oai_identifier': oai_identifier,
	}

	return render(request, template, context,content_type="application/xhtml+xml")
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
		'copyedits': models.CopyeditAssignment.objects.filter(copyeditor=request.user, completed__isnull=True),
		'new_task_form': new_task_form,
		'user_submissions': models.Book.objects.filter(owner=request.user),
		'author_copyedit_tasks': logic.author_tasks(request.user),
		'indexes': models.IndexAssignment.objects.filter(indexer=request.user, completed__isnull=True),
		'typesetting': models.TypesetAssignment.objects.filter((Q(requested__isnull=False) & Q(completed__isnull=True)) | (Q(typesetter_invited__isnull=False) & Q(typesetter_completed__isnull=True)), typesetter=request.user),
		'user_proposals': submission_models.Proposal.objects.filter(owner=request.user)
	}

	return render(request, template, context)


@login_required
def user_submission(request, submission_id):
	book = get_object_or_404(models.Book, pk=submission_id, owner=request.user)

	template = 'core/user/user_submission.html'
	context = {
		'submission': book,
		'active': 'user_submission',
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
				return redirect(reverse('login'))
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
def overview(request):

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
	if new_task_form.is_valid():
		task = new_task_form.save(commit=False)
		task.creator = request.user
		task.assignee = request.user
		task.save()

		return HttpResponse(json.dumps({'id': task.pk,'text': task.text}))
	else:
		return HttpResponse(new_task_form.errors)

@csrf_exempt
@is_book_editor_or_author
def new_message(request, submission_id):

	new_message_form = forms.MessageForm(request.POST)
	if new_message_form.is_valid():
		new_message = new_message_form.save(commit=False)
		new_message.sender = request.user
		new_message.book = get_object_or_404(models.Book, pk=submission_id)
		new_message.save()

		response_dict = {
			'status_code': 200, 
			'message_id': new_message.pk,
			'sender': '%s %s' % (new_message.sender.first_name, new_message.sender.last_name),
			'message': new_message.message,
			'date_sent': new_message.date_sent.strftime("%-d %b %Y, %H:%M"),
		}

		return HttpResponse(json.dumps(response_dict))
	else:
		return HttpResponse(json.dumps(new_message_form.errors))

@csrf_exempt
@is_book_editor_or_author
def get_messages(request, submission_id):
	try:
		last_message = int(request.GET.get('last_message', 0))
		messages = models.Message.objects.filter(book__pk=submission_id, pk__gt=last_message).exclude(sender=request.user).order_by('-id')

		message_list = [{
				'message': message.message,
				'message_id': message.pk,
				'sender': '%s %s' % (message.sender.first_name, message.sender.last_name),
				'initials': message.sender.profile.initials(),
				'message': message.message,
				'date_sent': message.date_sent.strftime("%-d %b %Y, %H:%M"),
				'user':'same',
			} for message in messages
		]
		response_dict = {
			'status_code': 200,
			'messages': message_list,
		}

		return HttpResponse(json.dumps(response_dict))
	except Exception, e:
		print e



def get_authors(request, submission_id):
    if request.is_ajax():
        q = request.GET.get('term', '')
        data = json.dumps(logic.get_author_emails(submission_id,q))
    else:
        data = 'Unable to get authors'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def get_editors(request, submission_id):
    if request.is_ajax():
	    q = request.GET.get('term', '')
	    results = []
	    data = json.dumps(logic.get_editor_emails(submission_id,q))
    else:
		data = 'Unable to get editors'

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def get_onetaskers(request, submission_id):
    if request.is_ajax():
        q = request.GET.get('term', '')
        data = json.dumps(logic.get_onetasker_emails(submission_id,q))
    else:
        data = 'Unable to get onetaskers'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def get_all(request, submission_id):
    submission = get_object_or_404(models.Book, pk=submission_id)
    if request.is_ajax():
        q = request.GET.get('term', '')
        onetasker_results = logic.get_onetasker_emails(submission_id,q)
        editor_results = logic.get_editor_emails(submission_id,q)
        author_results = logic.get_author_emails(submission_id,q)
        results = []
        for user in onetasker_results:
        	if not string_any(user['value'] in result['value'] for result in results):

        	   results.append(user)
        for author in author_results:
        	if not string_any(author['value'] in result['value'] for result in results):
        	    results.append(author)
        	    
        for editor in editor_results:
        	if not string_any(editor['value'] in result['value'] for result in results):
        	    results.append(editor)
        data = json.dumps(results)
    else:
        data = 'Unable to get any user'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

@login_required
def email_users(request, group, submission_id=None, user_id=None):
	submission = get_object_or_404(models.Book, pk=submission_id)
	editors = logic.get_editors(submission)
	authors = submission.author.all()
	onetaskers = submission.onetaskers()
	to_value=""
	sent = False
	if request.POST:
		print "sS"
		attachment = request.FILES.get('attachment')
		subject = request.POST.get('subject')
		body = request.POST.get('body')
		
		to_addresses = request.POST.get('to_values').split(';')
		cc_addresses = request.POST.get('cc_values').split(';')
		bcc_addresses = request.POST.get('bcc_values').split(';')

		to_list=logic.clean_email_list(to_addresses)
		cc_list=logic.clean_email_list(cc_addresses)
		bcc_list=logic.clean_email_list(bcc_addresses)
		
		if attachment: 
			attachment = handle_file(attachment, submission, 'other', request.user, "Attachment: Uploaded by %s" % (request.user.username))
		
		if to_addresses:
			if attachment: 
				send_email(subject=subject, context={}, from_email=request.user.email, to=to_list, bcc=bcc_list,cc=cc_list, html_template=body, book=submission, attachment=attachment)
			else:
				send_email(subject=subject, context={}, from_email=request.user.email, to=to_list,bcc=bcc_list,cc=cc_list, html_template=body, book=submission)
			message ="E-mail with subject '%s' was sent." % (subject)
			return HttpResponse('<script type="text/javascript">window.alert("'+message+'")</script><script type="text/javascript">window.close()</script>') 

	if not group == "all" and user_id:
		
		if group == "editors":
			try:
				editor = models.User.objects.get(pk=user_id)
				if editor in editors:
					to_value="%s;" % (editor.email)
				else:
					messages.add_message(request, messages.ERROR, "This editor is not an editor of this submission")
			except models.User.DoesNotExist:
				messages.add_message(request, messages.ERROR, "This editor was not found")

		elif group == "authors":
			author = get_object_or_404(models.Author, pk=user_id)
			authors = submission.author.all()
			if author in authors:
				to_value="%s;" % (author.author_email)
			else:
				messages.add_message(request, messages.ERROR, "This author is not an author of this submission")

		elif group == "onetaskers":
			user = get_object_or_404(models.User, pk=user_id)
			if user in onetaskers:
				to_value="%s;" % (user.email)
			else:
				messages.add_message(request, messages.ERROR, "This onetasker was not found")

	elif group =="all" and user_id:
		messages.add_message(request, messages.ERROR, "Cannot use the user field on this page because of the 'all' in the url. Try replacing it with other email groups: 'authors' or 'editors' or 'onetaskers'")
	
	group_name=group
	
	if not group_name == "editors" and not group_name == "all" and not group_name == "authors" and not group_name == "onetaskers":
		messages.add_message(request, messages.ERROR, "Group type does not exist. Redirected to page of all groups")
		return redirect(reverse('email_users', kwargs={'group':'all','submission_id': submission.id}))
	
	source = "/email/get/%s/submission/%s/" % (group_name,submission_id)

	template = 'core/email.html'
	context = {
		'submission': submission,
		'from': request.user,
		'to_value':to_value,
		'source': source,
		'group': group_name,
		'user_id':user_id,
		'sent':sent,
		
	}
	return render(request, template, context)

@is_book_editor
def upload_misc_file(request, submission_id):

	submission = get_object_or_404(models.Book, pk=submission_id)
	if request.POST:
		file_form = forms.UploadMiscFile(request.POST)
		if file_form.is_valid():
			new_file = handle_file(request.FILES.get('misc_file'), submission, file_form.cleaned_data.get('file_type'), request.user, file_form.cleaned_data.get('label'))
			submission.misc_files.add(new_file)
			return redirect(reverse('editor_submission', kwargs={'submission_id': submission.id}))
	else:
		file_form = forms.UploadMiscFile()

	template = 'core/misc_files/upload.html'
	context = {
		'submission': submission,
		'file_form': file_form,
		'active_page':'editor_submission'
	}

	return render(request, template, context)
	
@login_required
def serve_marc21_file(request, submission_id,type):
	book = get_object_or_404(models.Book, pk=submission_id)
	if type=='xml':
		file_pk=logic.book_to_mark21_file(book,request.user,True)
	else:
		file_pk=logic.book_to_mark21_file(book,request.user)
	_file = get_object_or_404(models.File, pk=file_pk)
	file_path = os.path.join(settings.BOOK_DIR, submission_id, _file.uuid_filename)

	print file_path

	try:
		fsock = open(file_path, 'r')
		mimetype = mimetypes.guess_type(file_path)
		response = StreamingHttpResponse(fsock, content_type=mimetype)
		response['Content-Disposition'] = "attachment; filename=%s" % (_file.original_filename)
		log.add_log_entry(book=book, user=request.user, kind='file', message='File %s downloaded.' % _file.uuid_filename, short_name='Download')
		return response
	except IOError:
		messages.add_message(request, messages.ERROR, 'File not found. %s' % (file_path))
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@is_onetasker
def serve_file(request, submission_id, file_id):
	book = get_object_or_404(models.Book, pk=submission_id)
	_file = get_object_or_404(models.File, pk=file_id)
	file_path = os.path.join(settings.BOOK_DIR, submission_id, _file.uuid_filename)

	try:
		fsock = open(file_path, 'r')
		mimetype = mimetypes.guess_type(file_path)
		response = StreamingHttpResponse(fsock, content_type=mimetype)
		response['Content-Disposition'] = "attachment; filename=%s" % (_file.original_filename)
		log.add_log_entry(book=book, user=request.user, kind='file', message='File %s downloaded.' % _file.uuid_filename, short_name='Download')
		return response
	except IOError:
		messages.add_message(request, messages.ERROR, 'File not found. %s' % (file_path))
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@is_book_editor_or_author
def serve_versioned_file(request, submission_id, revision_id):
	book = get_object_or_404(models.Book, pk=submission_id)
	versions_file = get_object_or_404(models.FileVersion, pk=revision_id)
	file_path = os.path.join(settings.BOOK_DIR, submission_id, versions_file.uuid_filename)

	try:
		fsock = open(file_path, 'r')
		mimetype = mimetypes.guess_type(file_path)
		response = StreamingHttpResponse(fsock, content_type=mimetype)
		response['Content-Disposition'] = "attachment; filename=%s" % (versions_file.uuid_filename)
		log.add_log_entry(book=book, user=request.user, kind='file', message='File %s downloaded.' % versions_file.uuid_filename, short_name='Download')
		return response
	except IOError:
		messages.add_message(request, messages.ERROR, 'File not found. %s/%s' % (file_path, versions_file.uuid_filename))
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@is_book_editor_or_author
def delete_file(request, submission_id, file_id, returner):
	book = get_object_or_404(models.Book, pk=submission_id)
	_file = get_object_or_404(models.File, pk=file_id)
	file_id = _file.id
	_file.delete()

	if returner == 'new':
		return redirect(reverse('editor_submission', kwargs={'submission_id': book.id}))
	elif returner == 'review':
		return redirect(reverse('editor_review', kwargs={'submission_id': book.id}))
	elif returner == 'production':
		return redirect(reverse('editor_production', kwargs={'submission_id': book.id}))

@is_book_editor_or_author
def update_file(request, submission_id, file_id, returner):
	book = get_object_or_404(models.Book, pk=submission_id)
	_file = get_object_or_404(models.File, pk=file_id)
	if request.POST:
		label = request.POST['rename']
		if label:
			_file.label=label
			_file.save()

		for file in request.FILES.getlist('update_file'):
			handle_file_update(file, _file, book, _file.kind, request.user)
			messages.add_message(request, messages.INFO, 'File updated.')

		if returner == 'new':
			return redirect(reverse('editor_submission', kwargs={'submission_id': book.id}))
		elif returner == 'review':
			return redirect(reverse('editor_review', kwargs={'submission_id': book.id}))
		elif returner == 'production':
			return redirect(reverse('editor_production', kwargs={'submission_id': book.id}))

	template = 'core/update_file.html'
	context = {
		'submission': book,
		'file': _file,
		'update': True
	}

	return render(request, template, context)

@is_book_editor_or_author
def view_file(request, submission_id, file_id):
	book = get_object_or_404(models.Book, pk=submission_id)
	_file = get_object_or_404(models.File, pk=file_id)
	
	template = 'core/update_file.html'
	context = {
		'submission': book,
		'file': _file,
		'update': False
	}

	return render(request, template, context)

@is_book_editor_or_author
def versions_file(request, submission_id, file_id):
	book = get_object_or_404(models.Book, pk=submission_id)
	_file = get_object_or_404(models.File, pk=file_id)
	versions = models.FileVersion.objects.filter(file=_file).extra(order_by = ['date_uploaded'])

	template = 'core/versions_file.html'
	context = {
		'submission': book,
		'file': _file,
		'versions': versions
	}

	return render(request, template, context)

# Log
@is_book_editor
def view_log(request, submission_id):
	book = get_object_or_404(models.Book, pk=submission_id)
	log_list = models.Log.objects.filter(book=book).order_by('-date_logged')
	email_list = models.EmailLog.objects.filter(book=book).order_by('-sent')

	template = 'editor/log.html'
	context = {
		'submission': book,
		'log_list': log_list,
		'email_list': email_list,
		'active': 'log',
	}

	return render(request, template, context)

## PROPOSALS ##

@is_editor
def proposal(request):
	proposal_list = submission_models.Proposal.objects.filter((~Q(status='declined') & ~Q(status='accepted')))
	proposals = []
	for proposal in proposal_list:
		if not proposal.requestor:
			proposals.append(proposal)
		elif proposal.requestor==request.user:
			proposals.append(proposal)
	template = 'core/proposals/proposal.html'
	context = {
		'proposal_list': proposals,
	}

	return render(request, template, context)

@is_editor
def view_proposal(request, proposal_id):
	proposal = get_object_or_404(submission_models.Proposal, pk=proposal_id)
	relationships = models.ProposalFormElementsRelationship.objects.filter(form=proposal.form)
	data = json.loads(proposal.data)

	template = 'core/proposals/view_proposal.html'
	context = {
		'proposal': proposal,
		'relationships':relationships,
		'data':data,
	}

	return render(request, template, context)

@is_editor
def start_proposal_review(request, proposal_id):
	proposal = get_object_or_404(submission_models.Proposal, pk=proposal_id, date_review_started__isnull=True)
	reviewers = models.User.objects.filter(profile__roles__slug='reviewer')
	committees = manager_models.Group.objects.filter(group_type='review_committee')
	email_text = models.Setting.objects.get(group__name='email', name='proposal_review_request').value
	start_form = submission_forms.ProposalStart()

	if request.POST:
		start_form = submission_forms.ProposalStart(request.POST, instance=proposal)
		if start_form.is_valid():
			proposal = start_form.save(commit=False)
			proposal.date_review_started = timezone.now()
			due_date = request.POST.get('due_date')
			email_text = request.POST.get('email_text')
			print email_text
			reviewers = User.objects.filter(pk__in=request.POST.getlist('reviewer'))
			committees = manager_models.Group.objects.filter(pk__in=request.POST.getlist('committee'))

			# Handle reviewers
			for reviewer in reviewers:
				new_review_assignment = submission_models.ProposalReview(
					user=reviewer,
					proposal=proposal,
					due=due_date,
				)

				try:
					new_review_assignment.save()
					proposal.review_assignments.add(new_review_assignment)
					logic.send_proposal_review_request(proposal, new_review_assignment, email_text)
				except IntegrityError:
					messages.add_message(request, messages.WARNING, '%s %s is already a reviewer' % (reviewer.first_name, reviewer.last_name))

			# Handle committees
			for committee in committees:
				members = manager_models.GroupMembership.objects.filter(group=committee)
				for member in members:
					new_review_assignment = submission_models.ProposalReview(
						user=member.user,
						proposal=proposal,
						due=due_date,
					)

					try:
						new_review_assignment.save()
						proposal.review_assignments.add(new_review_assignment)
						logic.send_proposal_review_request(proposal, new_review_assignment, email_text)
					except IntegrityError:
						messages.add_message(request, messages.WARNING, '%s %s is already a reviewer' % (member.user.first_name, member.user.last_name))

			# Tidy up and save

			proposal.date_review_started = timezone.now()
			proposal.save()

			return redirect(reverse('view_proposal', kwargs={'proposal_id': proposal.id}))

	template = 'core/proposals/start_proposal_review.html'
	context = {
		'proposal': proposal,
		'start_form': start_form,
		'reviewers': reviewers,
		'committees': committees,
		'email_text':email_text,
	}

	return render(request, template, context)

	template = 'core/proposals/start_proposal_review.html'
	context = {
		'proposal': proposal,
		'start_form': start_form,
		'reviewers': reviewers,
		'committees': committees,
		'email_text':email_text,
	}

	return render(request, template, context)

@is_editor
def view_proposal_review_decision(request, proposal_id, assignment_id):

	proposal = get_object_or_404(submission_models.Proposal, pk=proposal_id)
	review_assignment = get_object_or_404(submission_models.ProposalReview, pk=assignment_id)
	
	if request.POST:
		if 'accept' in request.POST:
			review_assignment.accepted = timezone.now()
			message = "Review Assignment request for '%s' has been accepted by %s %s."  % (submission.title,review_assignment.user.first_name, review_assignment.user.last_name)
			log.add_log_entry(book=submission, user=request.user, kind='review', message=message, short_name='Assignment accepted')
			logic.notify_editors(submission,message,editors,request.user,'review')
				
		elif 'decline' in request.POST:
			review_assignment.declined = timezone.now()
			message = "Review Assignment request for '%s' has been declined by %s %s."  % (submission.title,review_assignment.user.first_name, review_assignment.user.last_name)
			logic.notify_editors(submission,message,editors,request.user,'review')
			log.add_log_entry(book=submission, user=request.user, kind='review', message=message, short_name='Assignment declined')
	
	
	template = 'core/proposals/decision_review_assignment.html'
	context = {
		'proposal': proposal,
		'review': review_assignment,
		'result': result,
		'active': 'proposal_review',
	}

	return render(request, template, context)

@is_editor
def view_proposal_review(request, proposal_id, assignment_id):

	proposal = get_object_or_404(submission_models.Proposal, pk=proposal_id)
	review_assignment = get_object_or_404(submission_models.ProposalReview, pk=assignment_id)
	result = review_assignment.results
	form = review_forms.GeneratedForm(form=proposal.review_form)

	ci_required = models.Setting.objects.get(group__name='general', name='ci_required')
	recommendation_form = forms.RecommendationForm(ci_required=ci_required.value)
	if result:
		relations = review_models.FormElementsRelationship.objects.filter(form=result.form)
		data_ordered = logic.order_data(logic.decode_json(result.data), relations)
	else:
		relations = None
		data_ordered = None

	template = 'core/proposals/review_assignment.html'
	context = {
		'proposal': proposal,
		'review': review_assignment,
		'data_ordered': data_ordered,
		'result': result,
		'form':form,
		'recommendation_form':recommendation_form,
		'active': 'proposal_review',
	}

	return render(request, template, context)

@is_editor
def add_proposal_reviewers(request, proposal_id):

	proposal = get_object_or_404(submission_models.Proposal, pk=proposal_id)
	reviewers = models.User.objects.filter(profile__roles__slug='reviewer')
	committees = manager_models.Group.objects.filter(group_type='review_committee')
	email_text = models.Setting.objects.get(group__name='email', name='proposal_review_request').value

	if request.POST:
		due_date = request.POST.get('due_date')
		reviewers = User.objects.filter(pk__in=request.POST.getlist('reviewer'))
		committees = manager_models.Group.objects.filter(pk__in=request.POST.getlist('committee'))
		email_text = request.POST.get('email_text')
		print email_text

		# Handle reviewers
		for reviewer in reviewers:
			new_review_assignment = submission_models.ProposalReview(
				user=reviewer,
				proposal=proposal,
				due=due_date,
			)

			try:
				new_review_assignment.save()
				proposal.review_assignments.add(new_review_assignment)
				logic.send_proposal_review_request(proposal, new_review_assignment, email_text)
			except IntegrityError:
				messages.add_message(request, messages.WARNING, '%s %s is already a reviewer' % (reviewer.first_name, reviewer.last_name))

		# Handle committees
		for committee in committees:
			members = manager_models.GroupMembership.objects.filter(group=committee)
			for member in members:
				new_review_assignment = submission_models.ProposalReview(
					user=reviewer,
					proposal=proposal,
					due=due_date,
				)

				try:
					new_review_assignment.save()
					proposal.review_assignments.add(new_review_assignment)
					logic.send_proposal_review_request(proposal, new_review_assignment, email_text)
				except IntegrityError:
					messages.add_message(request, messages.WARNING, '%s %s is already a reviewer' % (member.user.first_name, member.user.last_name))

		# Tidy up and save

		proposal.date_review_started = timezone.now()
		proposal.save()

		return redirect(reverse('view_proposal', kwargs={'proposal_id': proposal.id}))

	template = 'core/proposals/add_reviewers.html'
	context = {
		'proposal': proposal,
		'reviewers': reviewers,
		'committees': committees,
		'email_text':email_text,
	}

	return render(request, template, context)

@is_editor
def decline_proposal(request, proposal_id):

	proposal = get_object_or_404(submission_models.Proposal, pk=proposal_id)
	email_text = models.Setting.objects.get(group__name='email', name='proposal_decline')

	if request.POST:
		proposal.status = 'declined'
		logic.close_active_reviews(proposal)
		proposal.requestor=request.user
		proposal.save()
		logic.send_proposal_decline(proposal, email_text=request.POST.get('decline-email'), sender=request.user)
		return redirect(reverse('proposals'))

	template = 'core/proposals/decline_proposal.html'
	context = {
		'proposal': proposal,
		'email_text': logic.setting_template_loader(setting=email_text,path="core/proposals/",pattern="email_template_",dictionary={'sender':request.user,'receiver':proposal.owner}),
	}

	return render(request, template, context)


@is_editor
def accept_proposal(request, proposal_id):
	'Marks a proposal as accepted, creates a submission and emails the user'
	proposal = get_object_or_404(submission_models.Proposal, pk=proposal_id)
	email_text = models.Setting.objects.get(group__name='email', name='proposal_accept')

	if request.POST:
		proposal.status = 'accepted'
		logic.close_active_reviews(proposal)
		proposal.requestor=request.user
		submission = logic.create_submission_from_proposal(proposal, proposal_type=request.POST.get('proposal-type'))
		attachment = handle_attachment(request, submission)
		logic.send_proposal_accept(proposal, email_text=request.POST.get('accept-email'), submission=submission, sender=request.user, attachment=attachment)
		proposal.save()
		return redirect(reverse('proposals'))

	template = 'core/proposals/accept_proposal.html'
	
	context = {
		'proposal': proposal,
		'email_text': logic.setting_template_loader(setting=email_text,path="core/proposals/",pattern="email_template_",dictionary={'sender':request.user,'receiver':proposal.owner}),
	}

	return render(request, template, context)

@is_editor
def request_proposal_revisions(request, proposal_id):

	proposal = get_object_or_404(submission_models.Proposal, pk=proposal_id)
	email_text = models.Setting.objects.get(group__name='email', name='proposal_request_revisions')

	if request.POST:
		proposal.status = 'revisions_required'
		logic.close_active_reviews(proposal)
		proposal.requestor=request.user
		logic.send_proposal_revisions(proposal, email_text=request.POST.get('revisions-email'), sender=request.user)
		proposal.save()
		return redirect(reverse('proposals'))

	template = 'core/proposals/revisions_proposal.html'
	context = {
		'proposal': proposal,
		'email_text': logic.setting_template_loader(setting=email_text,path="core/proposals/",pattern="email_template_",dictionary={'sender':request.user,'receiver':proposal.owner}),
	}

	return render(request, template, context)



## END PROPOSAL ##

