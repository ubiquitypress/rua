from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.db.models import Max
from django.utils import timezone
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

def create_new_review_round(book):
	latest_round = models.ReviewRound.objects.filter(book=book).aggregate(max=Max('round_number'))
	next_round = latest_round.get('max')+1 if latest_round.get('max') > 0 else 1
	return models.ReviewRound.objects.create(book=book, round_number=next_round)

def build_time_line_editing_copyedit(copyedit):
	timeline = []

	
	overdue = False
	if copyedit.accepted:
		if copyedit.completed and copyedit.completed > copyedit.due:
			overdue=True
		timeline.append({'stage': 'Requested', 'date': copyedit.requested,'overdue':overdue   })
		timeline.append({'stage': 'Accepted', 'date': copyedit.accepted,'overdue':overdue  })
		timeline.append({'stage': 'Editor Review', 'date': copyedit.editor_review,'overdue':overdue  })
		timeline.append({'stage': 'Author Invited', 'date': copyedit.author_invited,'overdue':overdue  })
		timeline.append({'stage': 'Author completed', 'date': copyedit.author_completed,'overdue':overdue  })
		if copyedit.completed:
			if overdue:
				timeline.append({'stage': 'Due', 'date': copyedit.due,'overdue':overdue  })
				timeline.append({'stage': 'Completed', 'date': copyedit.completed,'overdue':overdue  })
			else:
				timeline.append({'stage': 'Completed', 'date': copyedit.completed,'overdue':overdue  })
				timeline.append({'stage': 'Due', 'date': copyedit.due,'overdue':overdue  })
		else:
			timeline.append({'stage': 'Due', 'date': copyedit.due,'overdue':overdue  })
	else:
		timeline.append({'stage': 'Requested', 'date': copyedit.requested,'overdue':overdue   })
		timeline.append({'stage': 'Declined', 'date': copyedit.declined,'declined': True })
		timeline.append({'stage': 'Due', 'date': copyedit.due,'overdue':overdue   })

	return timeline
def build_time_line_editing_indexer(index):
	timeline = []

	overdue = False
	if index.accepted:
		if index.completed and index.completed > index.due:
			overdue=True
		timeline.append({'stage': 'Requested', 'date': index.requested,'overdue':overdue  })
		timeline.append({'stage': 'Accepted', 'date': index.accepted,'overdue':overdue  })
		if index.completed:
			if overdue:
				timeline.append({'stage': 'Due', 'date': index.due,'overdue':overdue })
				timeline.append({'stage': 'Completed', 'date': index.completed,'overdue':overdue })
			else:
				timeline.append({'stage': 'Completed', 'date': index.completed,'overdue':overdue  })
				timeline.append({'stage': 'Due', 'date': index.due,'overdue':overdue   })
		else:
			timeline.append({'stage': 'Due', 'date': index.due,'overdue':overdue   })
	else:
		timeline.append({'stage': 'Declined', 'date': index.declined,'declined': True  })
		timeline.append({'stage': 'Due', 'date': index.due,'overdue':overdue   })

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

# Email handler - should be moved to logic!
def send_proposal_review_request(proposal, review_assignment, email_text):
	from_email = models.Setting.objects.get(group__name='email', name='from_address')
	base_url = models.Setting.objects.get(group__name='general', name='base_url')

	review_url = 'http://%s/review/%s/%s/' % (base_url.value, 'proposal', proposal.id)

	context = {
		'review': review_assignment,
		'review_url': review_url,
	}

	email.send_email('Proposal Review Request', context, from_email.value, review_assignment.user.email, email_text)
#### WORKFLOW Logic #####


def order_data(data, relations):
    ordered_data = []
    for relation in relations:
        if relation.element.name in data:
            ordered_data.append([relation.element.name, data[relation.element.name]])
    return ordered_data

def decode_json(json_data):
    return json.loads(json_data)

def encode_data(data):
    return json.dumps(data)



def close_active_reviews(proposal):
    for review in proposal.review_assignments.all():
        review.completed = timezone.now()
        review.save()

def create_submission_from_proposal(proposal, proposal_type):
    book = models.Book(title=proposal.title, subtitle=proposal.subtitle,
        owner=proposal.owner, book_type=proposal_type, submission_stage=1)

    book.save()

    if book.book_type == 'monograph':
        submission_logic.copy_author_to_submission(proposal.owner, book)
    elif book.book_type == 'edited_volume':
        submission_logic.copy_editor_to_submission(proposal.owner, book)

    book.save()

    return book

def handle_typeset_assignment(book, typesetter, files, due_date, email_text, requestor, attachment):

    new_typesetter = models.TypesetAssignment(
        book=book,
        typesetter=typesetter,
        requestor=requestor,
        due=due_date,
    )

    new_typesetter.save()

    for _file in files:
        new_typesetter.files.add(_file)

    new_typesetter.save()

    send_invite_typesetter(book, new_typesetter, email_text, requestor, attachment)

    log.add_log_entry(book=book, user=requestor, kind='typeser', message='Typesetter %s %s assigned. Due %s' % (typesetter.first_name, typesetter.last_name, due_date), short_name='Typeset Assignment')

# Email Handlers - TODO: move to email.py?

def send_review_request(book, review_assignment, email_text, attachment=None):
    from_email = models.Setting.objects.get(group__name='email', name='from_address')
    base_url = models.Setting.objects.get(group__name='general', name='base_url')

    decision_url = 'http://%s/review/%s/%s/assignment/%s/decision/' % (base_url.value, review_assignment.review_type, book.id, review_assignment.id)

    context = {
        'book': book,
        'review': review_assignment,
        'decision_url': decision_url,
    }

    email.send_email('Review Request', context, from_email.value, review_assignment.user.email, email_text, book=book, attachment=attachment)

def send_proposal_decline(proposal, email_text, sender):
    from_email = models.Setting.objects.get(group__name='email', name='from_address')

    context = {
        'proposal': proposal,
        'sender': sender,
    }

    email.send_email('[abp] Proposal Declined', context, from_email.value, proposal.owner.email, email_text)

def send_proposal_accept(proposal, email_text, submission, sender, attachment=None):
    from_email = models.Setting.objects.get(group__name='email', name='from_address')

    context = {
        'base_url': models.Setting.objects.get(group__name='general', name='base_url').value,
        'proposal': proposal,
        'submission': submission,
        'sender': sender,
    }

    email.send_email('[abp] Proposal Accepted', context, from_email.value, proposal.owner.email, email_text, book=submission, attachment=attachment)

def send_proposal_revisions(proposal, email_text, sender):
    from_email = models.Setting.objects.get(group__name='email', name='from_address')

    context = {
        'base_url': models.Setting.objects.get(group__name='general', name='base_url').value,
        'proposal': proposal,
        'sender': sender,
    }

    email.send_email('[abp] Proposal Revisions Required', context, from_email.value, proposal.owner.email, email_text)


def send_author_sign_off(submission, email_text, sender):
    from_email = models.Setting.objects.get(group__name='email', name='from_address')

    context = {
        'base_url': models.Setting.objects.get(group__name='general', name='base_url').value,
        'submission': submission,
        'sender': sender,
    }

    email.send_email('Book Contract Uploaded', context, from_email.value, submission.owner.email, email_text, book=submission)


def send_invite_typesetter(book, typeset, email_text, sender, attachment):

    print attachment
    from_email = models.Setting.objects.get(group__name='email', name='from_address')

    context = {
        'base_url': models.Setting.objects.get(group__name='general', name='base_url').value,
        'submission': typeset.book,
        'typeset': typeset,
        'sender': sender,
    }

    email.send_email('Typesetting', context, from_email.value, typeset.typesetter.email, email_text, book=book, attachment=attachment)	
