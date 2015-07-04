from core import logic
from core.cache import cache_result

@cache_result(300)
def press(request):
	return {'press': logic.press_settings()}