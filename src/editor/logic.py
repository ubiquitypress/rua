from django.db.models import Q

from core import models

def get_submission_tasks(book, user):
	task_list = []
	base_url = models.Setting.objects.get(group__name='general', name='base_url').value

	copyedit_tasks = models.CopyeditAssignment.objects.filter(book=book, completed__isnull=False, editor_review__isnull=True, author_completed__isnull=True)
	typeset_tasks = models.TypesetAssignment.objects.filter((Q(completed__isnull=False) & Q(editor_review__isnull=True)) | (Q(author_completed__isnull=False) & Q(editor_second_review__isnull=True)), requestor=user)

	for copyedit in copyedit_tasks:
		task_list.append({'type': 'copyedit', 'book': copyedit.book, 'task': 'Copyedit Review', 'date': copyedit.completed, 'title': copyedit.book.title, 'url': 'http://%s/editor/submission/%s/editing/copyedit/%s/' % (base_url, copyedit.book.id, copyedit.id)})

	for typeset in typeset_tasks:
		task_list.append({'type': 'typeset', 'book': typeset.book, 'task': 'Typsetting Review', 'date': typeset.completed, 'title': typeset.book.title, 'url': 'http://%s/editor/submission/%s/editing/typeset/%s/' % (base_url, typeset.book.id, typeset.id)})

	return task_list