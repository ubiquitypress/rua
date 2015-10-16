from core import models
from core.cache import cache_result
from revisions import models as revisions_models

def author_tasks(user):
	base_url = models.Setting.objects.get(group__name='general', name='base_url').value
	task_list = []
	revision_tasks = revisions_models.Revision.objects.filter(book__owner=user, requested__isnull=False, completed__isnull=True)
	copyedit_tasks = models.CopyeditAssignment.objects.filter(book__owner=user, author_invited__isnull=False, author_completed__isnull=True)
	typeset_tasks = models.TypesetAssignment.objects.filter(book__owner=user, author_invited__isnull=False, author_completed__isnull=True)

	for revision in revision_tasks:
		task_list.append({'type': 'revisions', 'book': revision.book, 'task': 'Revisions', 'date': revision.due, 'title': revision.book.title, 'url': '/author/submission/%s/revisions/%s/' % (revision.book.id, revision.id)})

	for copyedit in copyedit_tasks:
		task_list.append({'type': 'copyedit', 'book': copyedit.book, 'task': 'Copyedit Review', 'date': copyedit.author_invited, 'title': copyedit.book.title, 'url': '/author/submission/%s/editing/copyedit/%s/' % (copyedit.book.id, copyedit.id)})

	for typeset in typeset_tasks:
		task_list.append({'type': 'typeset', 'book': typeset.book, 'task': 'Typsetting Review', 'date': typeset.author_invited, 'title': typeset.book.title, 'url': '/author/submission/%s/editing/typeset/%s/' % (typeset.book.id, typeset.id)})

	return task_list

def submission_tasks(book, user):
	task_list = []
	base_url = models.Setting.objects.get(group__name='general', name='base_url').value

	revision_tasks = revisions_models.Revision.objects.filter(book=book, requested__isnull=False, completed__isnull=True)
	copyedit_tasks = models.CopyeditAssignment.objects.filter(book=book, author_invited__isnull=False, author_completed__isnull=True)
	typeset_tasks = models.TypesetAssignment.objects.filter(book=book, author_invited__isnull=False, author_completed__isnull=True)

	for revision in revision_tasks:
		task_list.append({'type': 'revisions', 'book': revision.book, 'task': 'Revisions Requested', 'date': revision.due, 'title': revision.book.title, 'url': '/author/submission/%s/revisions/%s/' % (book.id, revision.id)})

	for copyedit in copyedit_tasks:
		task_list.append({'type': 'copyedit', 'book': copyedit.book, 'task': 'Copyedit Review', 'date': copyedit.author_invited, 'title': copyedit.book.title, 'url': '/author/submission/%s/editing/copyedit/%s/' % (copyedit.book.id, copyedit.id)})

	for typeset in typeset_tasks:
		task_list.append({'type': 'typeset', 'book': typeset.book, 'task': 'Typsetting Review', 'date': typeset.author_invited, 'title': typeset.book.title, 'url': 'uthor/submission/%s/editing/typeset/%s/' % (typeset.book.id, typeset.id)})

	return task_list