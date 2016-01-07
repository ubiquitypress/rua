from django.shortcuts import redirect, render, get_object_or_404, Http404
from django.contrib import messages
from django.core.urlresolvers import reverse

from core import models, logic as core_logic, task
from core.decorators import is_onetasker
from onetasker import forms
from core import log
import logic

from datetime import datetime



@is_onetasker
def dashboard(request):

	onetasker_tasks = core_logic.onetasker_tasks(request.user)

	template = 'onetasker/dashboard.html'
	context = {
		'completed_tasks': onetasker_tasks.get('completed'),
		'active_tasks': onetasker_tasks.get('active'),
		'completed_count':len(onetasker_tasks.get('completed')),
		'active_count':len(onetasker_tasks.get('active'))

	}

	return render(request, template, context)


def task_hub(request, assignment_type, assignment_id, about=None):

	assignment = logic.get_assignment(assignment_type, assignment_id)
	form = logic.get_assignemnt_form(request, assignment_type, assignment)
	center_block = 'onetasker/elements/submission_details.html' if about else 'onetasker/elements/files.html'
	right_block = logic.right_block(assignment)
	submitted_files = logic.get_submitted_files(assignment)

	if request.POST:
		#Handle decision
		decision = request.POST.get('decision', None)
		if decision == 'accept':
			assignment.accepted = datetime.now()
			assignment.save()
			return redirect(reverse('onetasker_task_hub', kwargs={'assignment_type': assignment_type, 'assignment_id': assignment_id}))
		elif decision == 'decline':
			assignment.declined = datetime.now()
			assignment.save()
			messages.add_message(request, messages.SUCCESS, 'Task declined.')
			return redirect(reverse('onetasker_task_hub_decline',kwargs={'assignment_type': assignment_type, 'assignment_id': assignment_id}))
		#handle submission
		elif 'task' in request.POST:

			form = logic.get_assignemnt_form(request, assignment_type, assignment)
			if form.is_valid():
				assignment = form.save(commit=False)
				files = request.FILES.getlist('file_upload')
				assignment = logic.handle_files(assignment, files)
				assignment.save()
				logic.notify_editor(assignment, '%s task completed' % (assignment.type()))
				messages.add_message(request, messages.SUCCESS, 'Task completed. Thanks!')
				return redirect(reverse('onetasker_task_hub', kwargs={'assignment_type': assignment_type, 'assignment_id': assignment_id}))
			else:
				print form

		#handle label
		elif 'label' in request.POST:
			_file = get_object_or_404(models.File, pk=request.POST.get('file_id'))
			_file.label = request.POST.get('label')
			_file.save()


	template = 'onetasker/taskhub.html'

	context = {
		'submission': assignment.book,
		'assignment':assignment,
		'form': form,
		'center_block': center_block,
		'right_block': right_block,
		'files':submitted_files,
		'about':about
	}

	return render(request, template, context)


@is_onetasker
def task_hub_decline(request, assignment_type, assignment_id,):

	assignment = logic.get_assignment(assignment_type, assignment_id)
	email_text = models.Setting.objects.get(group__name='email', name='task_decline')

	if request.POST:	
		if assignment_type == 'copyedit':
			format_kind = "copyedit"
			assignment_user = assignment.copyeditor 
		elif assignment_type == 'typesetting':
			format_kind = "typeset"
			assignment_user = assignment.typesetter 
		elif assignment_type == 'indexing':
			format_kind = "index"
			assignment_user = assignment.indexer 
		log.add_log_entry(book=assignment.book, user=request.user, kind=format_kind, message='%s assignment declined by %s.' % (assignment_type.title(),assignment_user.profile.full_name()), short_name='Assignment declined.')
		core_logic.send_task_decline(assignment=assignment, type=assignment_type, email_text=request.POST.get('decline-email'), sender=request.user)
		return redirect(reverse('user_dashboard'))

	template = 'onetasker/taskhub.html'
	context = {
		'submission': assignment.book,
		'assignment': assignment,
		'send_email':True,
		'center_block': 'onetasker/decline_contact.html',
		'email_text': core_logic.setting_template_loader(setting=email_text,path="onetasker/",pattern="email_template_",dictionary={'sender':request.user,'receiver':assignment.requestor}),
	}

	return render(request, template, context)



