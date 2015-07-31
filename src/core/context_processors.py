from core import logic
from core.cache import cache_result

@cache_result(300)
def press(request):
	return {'press': logic.press_settings()}

def task_count(request):
	return {'task_count': logic.task_count(request)}
