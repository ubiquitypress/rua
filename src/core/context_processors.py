from core import logic
from core.cache import cache_result

from django.contrib.auth.models import Group

@cache_result(300)
def press(request):
	return {'press': logic.press_settings()}

def task_count(request):
	try:
		return {'task_count': logic.task_count(request)}
	except:
		return 0

def user_groups(request):
	return {'groups': [group.name for group in request.user.groups_set.all()]}

