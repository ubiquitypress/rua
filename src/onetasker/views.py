from django.shortcuts import render
from core import models




def dashboard(request):

	completed_tasks = models.Task.objects.filter(assignee=request.user, completed__isnull=False)
	active_tasks = models.Task.objects.filter(assignee=request.user, completed__isnull=True)

	template = 'onetasker/dashboard.html'
	context = {
		'completed_tasks': completed_tasks,
		'active_tasks': active_tasks,
		'completed_count':completed_tasks.count(),
		'active_count':active_tasks.count()

	}

	return render(request, template, context)
