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

def task_count(request):
	# TODO: change this to be handled based on whether the user is logged in or not.
	try:
		return models.Task.objects.filter(assignee=request.user, completed__isnull=True).count()
	except TypeError:
		return 0

def author_tasks(user):
	base_url = models.Setting.objects.get(group__name='general', name='base_url').value
	task_list = []
	copyedit_tasks = models.CopyeditAssignment.objects.filter(book__owner=user, author_invited__isnull=False, author_completed__isnull=True)
	typeset_tasks = models.TypesetAssignment.objects.filter(book__owner=user, author_invited__isnull=False, author_completed__isnull=True)

	for copyedit in copyedit_tasks:
		task_list.append({'task': 'Copyedit Review', 'title': copyedit.book.title, 'url': 'http://%s/copyedit/book/%s/edit/%s/author/' % (base_url, copyedit.book.id, copyedit.id)})

	for typeset in typeset_tasks:
		task_list.append({'task': 'Typsetting Review', 'title': typeset.book.title, 'url': 'http://%s/typeset/book/%s/typeset/%s/author/' % (base_url, typeset.book.id, typeset.id)})

	return task_list