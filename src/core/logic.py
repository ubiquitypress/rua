from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from core import models
from core.cache import cache_result

from pprint import pprint

def send_email(subject, context, from_email, to, html_template, text_template=None):
	plaintext = get_template(text_template)
	htmly     = get_template(html_template)

	con = Context(context)

	text_content = plaintext.render(con)
	html_content = htmly.render(con)

	msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
	msg.attach_alternative(html_content, "text/html")
	msg.send()

@cache_result(300)
def press_settings():
	_dict = {}
	for group in models.SettingGroup.objects.all():
		_dict[group.name] = {setting.name:setting.value for setting in models.Setting.objects.filter(group=group)}

	return _dict