from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from core import models
from core.cache import cache_result
from django.db.models import Q

from revisions import models as revisions_models

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
	revision_tasks = revisions_models.Revision.objects.filter(book__owner=user, requested__isnull=False, completed__isnull=True)
	copyedit_tasks = models.CopyeditAssignment.objects.filter(book__owner=user, author_invited__isnull=False, author_completed__isnull=True)
	typeset_tasks = models.TypesetAssignment.objects.filter(book__owner=user, author_invited__isnull=False, author_completed__isnull=True)

	for revision in revision_tasks:
		task_list.append({'task': 'Revisions Requested', 'title': revision.book.title, 'url': 'http://%s/revisions/%s' % (base_url, revision.id)})

	for copyedit in copyedit_tasks:
		task_list.append({'task': 'Copyedit Review', 'title': copyedit.book.title, 'url': 'http://%s/copyedit/book/%s/edit/%s/author/' % (base_url, copyedit.book.id, copyedit.id)})

	for typeset in typeset_tasks:
		task_list.append({'task': 'Typsetting Review', 'title': typeset.book.title, 'url': 'http://%s/typeset/book/%s/typeset/%s/author/' % (base_url, typeset.book.id, typeset.id)})

	return task_list


def typesetter_tasks(user):

	pending = models.TypesetAssignment.objects.filter((Q(requested__isnull=False) & Q(completed__isnull=True)) | (Q(typesetter_invited__isnull=False) & Q(typsetter_completed__isnull=True)), typesetter=user)
	completed = models.TypesetAssignment.objects.filter(completed__isnull=False, typesetter=user).order_by('completed')

	return { 'pending':pending, 'completed':completed}
	
	

def copyeditor_tasks(user):

	pending = models.CopyeditAssignment.objects.filter(copyeditor=user, completed__isnull=True)
	print pending
	completed = models.CopyeditAssignment.objects.filter(copyeditor=user, completed__isnull=False).order_by('completed')

	return { 'pending':pending, 'completed':completed}

def indexer_tasks(user):

	pending = models.IndexAssignment.objects.filter(indexer=user, completed__isnull=True),
	completed = models.IndexAssignment.objects.filter(indexer=user, completed__isnull=False).order_by('completed')

	return { 'pending':pending, 'completed':completed}
	

def onetasker_tasks(user):
	active = []
	completed = []
	base_url = models.Setting.objects.get(group__name='general', name='base_url').value
	print type(copyeditor_tasks(user).get('completed'))

	for assignment in copyeditor_tasks(user).get('completed'):
		active.append({'assignment':assignment, 'type': 'Copyedit', 'url': 'http://%s/copyedit/book/%s/typeset/%s/author/' % (base_url, assignment.book.id, assignment.id)})

	for assignment in typesetter_tasks(user).get('completed'):
		active.append({'assignment':assignment, 'type': 'Typesetting', 'url': 'http://%s/typeset/book/%s/typeset/%s/author/' % (base_url, assignment.book.id, assignment.id)})
	
	for assignment in indexer_tasks(user).get('completed'):
		active.append({'assignment':assignment, 'type': 'Indexing', 'url': 'http://%s/indexing/book/%s/typeset/%s/author/' % (base_url, assignment.book.id, assignment.id)})

	for assignment in copyeditor_tasks(user).get('completed'):
		completed.append({'assignment':assignment, 'type': 'Copyedit', 'url': 'http://%s/copyedit/book/%s/typeset/%s/author/' % (base_url, assignment.book.id, assignment.id)})

	for assignment in typesetter_tasks(user).get('completed'):
		completed.append({'assignment':assignment, 'type': 'Typesetting', 'url': 'http://%s/typeset/book/%s/typeset/%s/author/' % (base_url, assignment.book.id, assignment.id)})
	
	for assignment in indexer_tasks(user).get('completed'):
		completed.append({'assignment':assignment, 'type': 'Indexing', 'url': 'http://%s/indexing/book/%s/typeset/%s/author/' % (base_url, assignment.book.id, assignment.id)})

	return {'completed':completed, 'active':active}
	