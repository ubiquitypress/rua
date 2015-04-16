from django.contrib.auth import authenticate
from django.contrib.auth import logout as logout_user
from django.contrib.auth import login as login_user
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django import forms

from submission import forms


def start_submission(request):

	proposal_form = forms.SubmitProposal()
	book_form = forms.SubmitBook()



	template = "submission/start_submission.html"

	context = {
	'proposal_form': proposal_form,
	'book_form': book_form
	}

	return render(request, template, context)


