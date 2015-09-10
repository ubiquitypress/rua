from django.db.models import Max
from django.utils import timezone

from core import models
from core import email
from core import log
from submission import logic as submission_logic

import json

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

def create_new_review_round(book):
	latest_round = models.ReviewRound.objects.filter(book=book).aggregate(max=Max('round_number'))
	next_round = latest_round.get('max')+1 if latest_round.get('max') > 0 else 1
	return models.ReviewRound.objects.create(book=book, round_number=next_round)

def close_active_reviews(proposal):
    for review in proposal.review_assignments.all():
        review.completed = timezone.now()
        review.save()

def create_submission_from_proposal(proposal, proposal_type):
    book = models.Book(title=proposal.title, subtitle=proposal.subtitle, description=proposal.description,
        owner=proposal.owner, book_type=proposal_type, submission_stage=1)

    book.save()

    if book.book_type == 'monograph':
        submission_logic.copy_author_to_submission(proposal.owner, book)
    elif book.book_type == 'edited_volume':
        submission_logic.copy_editor_to_submission(proposal.owner, book)

    book.save()

    return book

def handle_copyeditor_assignment(book, copyedit, files, due_date, email_text, requestor):
    
    new_copyeditor = models.CopyeditAssignment(
        book = book,
        copyeditor = copyedit,
        requestor = requestor,
        due = due_date,
    )

    new_copyeditor.save()

    for _file in files:
        new_copyeditor.files.add(_file)

    new_copyeditor.save()

    log.add_log_entry(book=book, user=requestor, kind='copyedit', message='Copyeditor %s %s assigned. Due %s' % (copyedit.first_name, copyedit.last_name, due_date), short_name='Copyedit Assignment')
    send_copyedit_assignment(book, new_copyeditor, email_text)

def handle_indexer_assignment(book, index, files, due_date, email_text, requestor):

    new_indexer = models.IndexAssignment(
        book=book,
        indexer=index,
        requestor=requestor,
        due=due_date,
    )

    new_indexer.save()

    for _file in files:
        new_indexer.files.add(_file)

    new_indexer.save()

    log.add_log_entry(book=book, user=requestor, kind='index', message='Indexer %s %s assigned. Due %s' % (index.first_name, index.last_name, due_date), short_name='Indexing Assignment')

def handle_typeset_assignment(book, typesetter, files, due_date, email_text, requestor):

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

    send_invite_typesetter(book, new_typesetter, email_text)

    log.add_log_entry(book=book, user=requestor, kind='typeser', message='Typesetter %s %s assigned. Due %s' % (typesetter.first_name, typesetter.last_name, due_date), short_name='Typeset Assignment')

# Email Handlers - TODO: move to email.py?

def send_proposal_decline(proposal, email_text):
    from_email = models.Setting.objects.get(group__name='email', name='from_address')

    context = {
        'proposal': proposal,
    }

    email.send_email('[abp] Proposal Declined', context, from_email.value, proposal.owner.email, email_text)

def send_proposal_accept(proposal, email_text, submission):
    from_email = models.Setting.objects.get(group__name='email', name='from_address')

    context = {
        'base_url': models.Setting.objects.get(group__name='general', name='base_url').value,
        'proposal': proposal,
        'submission': submission,
    }

    email.send_email('[abp] Proposal Accepted', context, from_email.value, proposal.owner.email, email_text)

def send_proposal_revisions(proposal, email_text):
    from_email = models.Setting.objects.get(group__name='email', name='from_address')

    context = {
        'base_url': models.Setting.objects.get(group__name='general', name='base_url').value,
        'proposal': proposal,
    }

    email.send_email('[abp] Proposal Revisions Required', context, from_email.value, proposal.owner.email, email_text)


def send_author_sign_off(submission, email_text):
    from_email = models.Setting.objects.get(group__name='email', name='from_address')

    context = {
        'base_url': models.Setting.objects.get(group__name='general', name='base_url').value,
        'submission': submission,
    }

    email.send_email('Book Contract Uploaded', context, from_email.value, submission.owner.email, email_text, book=submission)

def send_copyedit_assignment(submission, copyedit, email_text):
    from_email = models.Setting.objects.get(group__name='email', name='from_address')

    context = {
        'base_url': models.Setting.objects.get(group__name='general', name='base_url').value,
        'submission': submission,
        'copyedit': copyedit,
    }

    email.send_email('Copyedit Assignment', context, from_email.value, copyedit.copyeditor.email, email_text, book=submission)

def send_author_invite(submission, copyedit, email_text):
    from_email = models.Setting.objects.get(group__name='email', name='from_address')

    context = {
        'base_url': models.Setting.objects.get(group__name='general', name='base_url').value,
        'submission': submission,
        'copyedit': copyedit,
    }

    email.send_email('Copyediting Completed', context, from_email.value, submission.owner.email, email_text, book=submission)

def send_invite_typesetter(book, typeset, email_text):
    from_email = models.Setting.objects.get(group__name='email', name='from_address')

    context = {
        'base_url': models.Setting.objects.get(group__name='general', name='base_url').value,
        'submission': typeset.book,
        'typeset': typeset,
    }

    email.send_email('Typesetting', context, from_email.value, typeset.typesetter.email, email_text, book=book)
