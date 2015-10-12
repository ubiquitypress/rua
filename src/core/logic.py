from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from core.decorators import is_copyeditor, is_typesetter, is_indexer
from core import models
from core.cache import cache_result
from django.db.models import Q
from revisions import models as revisions_models

def clean_email_list(addresses):
	list_of_email_addresses=[]
	for address in addresses:
		if '@' in address:
			if address.replace(" ", "") not in list_of_email_addresses:
				list_of_email_addresses.append(address.replace(" ", ""))
	if len(list_of_email_addresses)<1:
		return None
	else:
		return list_of_email_addresses

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
def review_assignment_count(request):
	# TODO: change this to be handled based on whether the user is logged in or not.
	try:
		return models.ReviewAssignment.objects.filter(user=request.user, completed__isnull=True,declined__isnull=True).count()
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
		task_list.append({'task': 'Typesetting Review', 'title': typeset.book.title, 'url': 'http://%s/typeset/book/%s/typeset/%s/author/' % (base_url, typeset.book.id, typeset.id)})

	return task_list

def typesetter_tasks(user):

	active = models.TypesetAssignment.objects.filter((Q(requested__isnull=False) & Q(completed__isnull=True)) | (Q(typesetter_invited__isnull=False) & Q(typesetter_completed__isnull=True)), typesetter=user).exclude(declined__isnull=False)
	completed = models.TypesetAssignment.objects.filter((Q(completed__isnull=False) & Q(typesetter_completed__isnull=True)) | (Q(completed__isnull=False) & Q(typesetter_completed__isnull=False)), typesetter=user).order_by('-completed')[:5]

	return { 'active':active, 'completed':completed}
	
	
def copyeditor_tasks(user):

	active = models.CopyeditAssignment.objects.filter(copyeditor=user, completed__isnull=True).exclude(declined__isnull=False)
	completed = models.CopyeditAssignment.objects.filter(copyeditor=user, completed__isnull=False).order_by('-completed')[:5]

	return { 'active':active, 'completed':completed}

def indexer_tasks(user):

	active = models.IndexAssignment.objects.filter(indexer=user, completed__isnull=True).exclude(declined__isnull=False)
	completed = models.IndexAssignment.objects.filter(indexer=user, completed__isnull=False).order_by('-completed')[:5]

	return { 'active':active, 'completed':completed}
	

def onetasker_tasks(user):
	active = []
	completed = []

	active_copyeditor_tasks = copyeditor_tasks(user).get('active')
	completed_copyeditor_tasks = copyeditor_tasks(user).get('completed')
	active_typesetter_tasks = typesetter_tasks(user).get('active')
	completed_typesetter_tasks = typesetter_tasks(user).get('completed')
	active_indexer_tasks = indexer_tasks(user).get('active')
	completed_indexer_tasks = indexer_tasks(user).get('completed')


	for assignment in active_copyeditor_tasks:
		active.append({'assignment':assignment, 'type': 'copyedit', })

	for assignment in active_typesetter_tasks:
		active.append({'assignment':assignment, 'type': 'typesetting'})
	
	for assignment in active_indexer_tasks:
		print assignment
		active.append({'assignment':assignment, 'type': 'indexing'})

	for assignment in completed_copyeditor_tasks:
		completed.append({'assignment':assignment, 'type': 'copyedit'})

	for assignment in completed_typesetter_tasks:
		completed.append({'assignment':assignment, 'type': 'typesetting'})
	
	for assignment in completed_indexer_tasks:
		completed.append({'assignment':assignment, 'type': 'indexing'})

	return {'completed':completed, 'active':active}
def build_time_line_editing_copyedit(copyedit):
	timeline = []

	timeline.append({'stage': 'Requested', 'date': copyedit.requested })

	if copyedit.accepted:
		timeline.append({'stage': 'Accepted', 'date': copyedit.accepted })
		if copyedit.completed > copyedit.due:
			timeline.append({'stage': 'Due', 'date': copyedit.due,'overdue':True  })
			timeline.append({'stage': 'Completed', 'date': copyedit.completed,'overdue':True  })
		else:
			timeline.append({'stage': 'Completed', 'date': copyedit.completed,'overdue':False  })
			timeline.append({'stage': 'Due', 'date': copyedit.due,'overdue':False  })
		timeline.append({'stage': 'Editor Review', 'date': copyedit.editor_review })
		timeline.append({'stage': 'Author Invited', 'date': copyedit.author_invited })
		timeline.append({'stage': 'Author completed', 'date': copyedit.author_completed })
	else:
		timeline.append({'stage': 'Declined', 'date': copyedit.declined,'declined': True })
		timeline.append({'stage': 'Due', 'date': copyedit.due,'overdue':False   })

	return timeline
def build_time_line_editing_indexer(index):
	timeline = []

	timeline.append({'stage': 'Requested', 'date': index.requested })

	if index.accepted:
		timeline.append({'stage': 'Accepted', 'date': index.accepted })
		if index.completed > index.due:
			timeline.append({'stage': 'Due', 'date': index.due,'overdue':True })
			timeline.append({'stage': 'Completed', 'date': index.completed,'overdue':True })
		else:
			timeline.append({'stage': 'Completed', 'date': index.completed,'overdue':False  })

			timeline.append({'stage': 'Due', 'date': index.due,'overdue':False   })
	else:
		timeline.append({'stage': 'Declined', 'date': index.declined,'declined': True  })
		timeline.append({'stage': 'Due', 'date': index.due,'overdue':False   })

	return timeline
def build_time_line(book):
	timeline = []
	if book.stage:
		timeline.append({'stage': 'Proposal', 'date': book.stage.proposal})
		timeline.append({'stage': 'Submission', 'date': book.stage.submission})
		timeline.append({'stage': 'Review', 'date': book.stage.review})
		timeline.append({'stage': 'Internal Review', 'date': book.stage.internal_review})
		timeline.append({'stage': 'External Review', 'date': book.stage.external_review})
		timeline.append({'stage': 'Editing', 'date': book.stage.editing})
		timeline.append({'stage': 'Copyediting', 'date': book.stage.copyediting})
		timeline.append({'stage': 'Indexing', 'date': book.stage.indexing})
		timeline.append({'stage': 'Typesetting', 'date': book.stage.typesetting})
		timeline.append({'stage': 'Production', 'date': book.stage.production})
		timeline.append({'stage': 'Publication', 'date': book.stage.publication})
		timeline.append({'stage': 'Declined', 'date': book.stage.declined})

	return timeline
	
