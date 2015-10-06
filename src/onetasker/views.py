from django.shortcuts import render
from core import models
from core import logic as core_logic




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
