from django.shortcuts import render
from django.shortcuts import redirect, render, get_object_or_404, Http404

from core import models
from onetasker import forms
from core import logic as core_logic

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

	assignment = get_assignment(assignment_type, assignment_id)
	form = get_assignemnt_form(assignment_type, assignment)
	center_block = 'onetasker/elements/files.html'

	if assignment.accepted:
		right_block = 'onetasker/elements/task_form.html'
	else:
		right_block = None


	if request.POST:

		decision = request.POST.get('decision', None)
		if decision == 'accept':
			assignment.accepted = datetime.now()
			assignment.save()
		elif decision == 'decline':
			assignment.declined = datetime.now()
			assignment.save()
			return redirect(reverse('tasks'))




	template = 'onetasker/taskhub.html'

	context = {
		'submission': assignment.book,
		'assignment':assignment,
		'center_block': center_block,
		'right_block': right_block
	}

	return render(request, template, context)



###Helpers###

def get_assignment(assignment_type, assignment_id):
	''' given one of the 3 assignment types and it's id it returns an Assignment object'''

	if assignment_type == 'copyedit':
		assignment = get_object_or_404(models.CopyeditAssignment, pk=assignment_id)
	elif assignment_type == 'typesetting':
		assignment = get_object_or_404(models.TypesetAssignment, pk=assignment_id)
	elif assignment_type == 'indexing':
		assignment = get_object_or_404(models.IndexAssignment, pk=assignment_id)
	else:
		raise Http404

	return assignment

def get_assignemnt_form(assignment_type, assignment):

	if assignment_type == 'copyedit':
		form = forms.Copyedit(instance=assignment)
	elif assignment_type == 'typesetting':
		form = forms.Typeset(instance=assignment)
	elif assignment_type == 'indexing':
		form = forms.Index(instance=assignment)
	else:
		raise Http404

	return form

