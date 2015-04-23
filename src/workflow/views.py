from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import logout as logout_user
from django.contrib.auth import login as login_user
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q


from django.conf import settings

from core import models
from core import forms

from pprint import pprint

def new_submissions(request):

    submission_list = models.Book.objects.filter(stage__current_stage='submission')

    template = 'workflow/new_submissions.html'
    context = {
        'submission_list': submission_list,
    }

    return render(request, template, context)

def in_review(request):

    submission_list = models.Book.objects.filter(Q(stage__current_stage='i_review') | Q(stage__current_stage='e_review'))

    template = 'workflow/in_review.html'
    context = {
        'submission_list': submission_list,
    }

    return render(request, template, context)

def in_editing(request):

    submission_list = models.Book.objects.filter(Q(stage__current_stage='copy_editing') | Q(stage__current_stage='indexing'))

    template = 'workflow/in_editing.html'
    context = {
        'submission_list': submission_list,
    }

    return render(request, template, context)


def in_production(request):

    submission_list = models.Book.objects.filter(stage__current_stage='production')

    template = 'workflow/in_production.html'
    context = {
        'submission_list': submission_list,
    }

    return render(request, template, context)
