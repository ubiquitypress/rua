from django.contrib.auth import authenticate
from django.contrib.auth import logout as logout_user
from django.contrib.auth import login as login_user
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django import forms

from submission import forms

@login_required
def start_submission(request):

	book_form = forms.SubmitBook()

	template = "submission/start_submission.html"
	context = {
		'book_form': book_form,
	}

	return render(request, template, context)

@login_required
def start_proposal(request):

	proposal_form = forms.SubmitProposal()

	if request.method == 'POST':
		proposal_form = forms.SubmitProposal(request.POST, request.FILES)
		if proposal_form.is_valid():
			proposal = proposal_form.save(commit=False)
			proposal.owner = request.user
			proposal.save()
			messages.add_message(request, messages.SUCCESS, 'Proposal %s submitted' % proposal.id)
			return redirect(reverse('user_home'))


	template = "submission/start_proposal.html"
	context = {
		'proposal_form': proposal_form,
	}

	return render(request, template, context)
