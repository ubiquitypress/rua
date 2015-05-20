from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import logout as logout_user
from django.contrib.auth import login as login_user
from django.shortcuts import redirect, render, get_object_or_404
from django.http import Http404, HttpResponse, StreamingHttpResponse, HttpResponseRedirect
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
from core import log

from pprint import pprint
import os
import mimetypes

def new_submissions(request):

    submission_list = models.Book.objects.filter(stage__current_stage='submission')

    template = 'workflow/new_submissions.html'
    context = {
        'submission_list': submission_list,
        'active': 'new',
    }

    return render(request, template, context)

def view_new_submission(request, submission_id):

    submission = get_object_or_404(models.Book, pk=submission_id)

    template = 'workflow/view_new_submission.html'
    context = {
        'submission': submission,
        'active': 'new',
    }

    return render(request, template, context)

def in_review(request):

    submission_list = models.Book.objects.filter(Q(stage__current_stage='i_review') | Q(stage__current_stage='e_review'))

    template = 'workflow/in_review.html'
    context = {
        'submission_list': submission_list,
        'active': 'review',
    }

    return render(request, template, context)

def in_editing(request):

    submission_list = models.Book.objects.filter(Q(stage__current_stage='copy_editing') | Q(stage__current_stage='indexing'))

    template = 'workflow/in_editing.html'
    context = {
        'submission_list': submission_list,
        'active': 'editing',
    }

    return render(request, template, context)


def in_production(request):

    submission_list = models.Book.objects.filter(stage__current_stage='production')

    template = 'workflow/in_production.html'
    context = {
        'submission_list': submission_list,
        'active': 'production',
    }

    return render(request, template, context)

# Log

def view_log(request, submission_id):
    book = get_object_or_404(models.Book, pk=submission_id)
    log_list = models.Log.objects.filter(book=book)

    template = 'workflow/log.html'
    context = {
        'book': book,
        'log_list': log_list,
    }

    return render(request, template, context)

# File Handlers - should this be in Core?

def serve_file(request, submission_id, file_id):
    book = get_object_or_404(models.Book, pk=submission_id)
    _file = get_object_or_404(models.File, pk=file_id)
    file_path = os.path.join(settings.BOOK_DIR, submission_id, _file.uuid_filename)

    log.add_log_entry(book=book, user=request.user, kind='file', message='File %s downloaded.' % _file.uuid_filename, short_name='Download')

    try:
        fsock = open(file_path, 'r')
        mimetype = mimetypes.guess_type(file_path)
        response = StreamingHttpResponse(fsock, content_type=mimetype)
        response['Content-Disposition'] = "attachment; filename=%s" % (_file.uuid_filename)
        return response
    except IOError:
        messages.add_message(request, messages.ERROR, 'File not found. %s/%s' % (file_path, _file.uuid_filename))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def delete_file(request, submission_id, file_id):
    _file = get_object_or_404(models.File, pk=file_id)


