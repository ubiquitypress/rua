from core import models

def get_setting(setting_name, setting_group_slug, default=None):

	try:
		setting = models.Setting.objects.get(name=setting_name, group__slug=setting_group_slug)
		return setting.value
	except models.Setting.DoesNotExist:
		if default:
			return default
		else: 
			return ''
