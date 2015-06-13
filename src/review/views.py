from django.shortcuts import redirect, render, get_object_or_404

from core import models as core_models
from review import forms
from review import forms

def review(request, review_type, submission_id, access_key=None):

	if access_key:
		review_assignment = get_object_or_404(core_models.ReviewAssignment, access_key=access_key)
		submission = get_object_or_404(core_models.Book, pk=submission_id)
	else:
		submission = get_object_or_404(core_models.Book, pk=submission_id)
		review_assignment = get_object_or_404(core_models.ReviewAssignment, user=request.user, book=submission)

	form = forms.GeneratedForm(form=submission.review_form)

	template = 'review/review.html'
	context = {
		'review_assignment': review_assignment,
		'submission': submission,
		'form': form,
	}

	return render(request, template, context)
