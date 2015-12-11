from core import logic
from core.cache import cache_result

from django.contrib.auth.models import Group
from core import logic
from author.logic import author_tasks

@cache_result(300)
def press(request):
	return {'press': logic.press_settings()}

def task_count(request):
	try:
		return {'task_count': logic.task_count(request)}
	except:
		return {'task_count': 0}
def review_assignment_count(request):
	try:
		return {'review_assignment_count': logic.review_assignment_count(request)}
	except:
		return {'review_assignment_count': 0}

def onetasker_task_count(request):
	try:
		onetasker_tasks = logic.onetasker_tasks(request.user)
		return {'onetasker_task_count':  len(onetasker_tasks.get('active')),}
	except:
		return {'onetasker_task_count':  0}
def author_task_count(request):
	try:
		return {'author_task_count':  len(author_tasks(request.user))}
	except:
		return {'author_task_count':  0}

def roles(request):
	try:
		if not request.user.is_anonymous():
			return {'roles': [role.slug for role in request.user.profile.roles.all()]}
		else:
			return {'roles': ''}
	except:
		return {'roles': ''}

def domain(request):
	try:
		return {'domain': request.get_host()}
	except:
		pass

