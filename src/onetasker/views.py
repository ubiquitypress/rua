from django.shortcuts import render
from django.shortcuts import redirect, render, get_object_or_404, Http404
from django.contrib import messages

from core import models, logic as core_logic, task as notify
from onetasker import forms

import logic

from datetime import datetime




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


def task_hub(request, assignment_type, assignment_id):

	assignment = logic.get_assignment(assignment_type, assignment_id)
	form = logic.get_assignemnt_form(request, assignment_type, assignment)
	center_block = 'onetasker/elements/files.html'
	right_block = logic.right_block(assignment)

	if request.POST:
		#Handle decision
		decision = request.POST.get('decision', None)
		if decision == 'accept':
			assignment.accepted = datetime.now()
			assignment.save()
		elif decision == 'decline':
			assignment.declined = datetime.now()
			assignment.save()

			return redirect(reverse('tasks'))

		#handle submission
		elif 'task' in request.POST:
			form = logic.get_assignemnt_form(request, assignment_type, assignment)
			if form.is_valid():
				assignment = form.save(commit=False)
				files = request.FILES.getlist('file_upload'):
				assignment = logic.handle_files(assignment, files)
				for _file in request.FILES.getlist('file_upload'):
					new_file = logic.handle_file(_file, assignment)
					assignment = logic.add_file(assignment, new_file)
				assignment = logic.complete_task(assignment)
				assignment.save()
				logic.notify_editor(assignment)
				messages.add_message(request, messages.SUCCESS, 'Task completed. Thanks!')
			


	template = 'onetasker/taskhub.html'

	context = {
		'submission': assignment.book,
		'assignment':assignment,
		'form': form,
		'center_block': center_block,
		'right_block': right_block
	}

	return render(request, template, context)






