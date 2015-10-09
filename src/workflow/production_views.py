from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.models import User

from core import models
from core import log
from core import email
from core.decorators import is_book_editor
from core.cache import cache_result
from typeset import forms
from workflow import logic
from workflow import forms
from workflow.views import handle_file, handle_file_update, handle_attachment
from typeset import forms as typeset_forms

from pprint import pprint

## PRODUCTION ##

@is_book_editor
def view_production(request, submission_id):
	book = get_object_or_404(models.Book, pk=submission_id)
	typeset_assignments = models.TypesetAssignment.objects.filter(book=book)

	if request.POST and request.GET.get('start', None):
		if request.GET.get('start') == 'typesetting':
			book.stage.typesetting = timezone.now()
			book.stage.save()

	template = 'workflow/production/view.html'
	context = {
		'active': 'production',
		'submission': book,
		'format_list': models.Format.objects.filter(book=book).select_related('file'),
		'chapter_list': models.Chapter.objects.filter(book=book).select_related('file'),
		'typeset_assignments': typeset_assignments,
	}

	return render(request, template, context)



