from django.contrib import messages
from django.db.models import Max, Q
from django.utils.encoding import smart_text

from core import models, email, log
from core.util import get_setting


def generate_digital_choices(digital_formats):
    return [('', '------')] + [
        (fmt.id, "%s - %s" % (fmt.name, fmt.get_file_type_display()))
        for fmt in digital_formats
    ]


def generate_physical_choices(physical_formats):
    return [('', '------')] + [
        (frmt.id, "%s - %s" % (frmt.name, frmt.get_file_type_display()))
        for frmt in physical_formats
    ]


def send_new_user_ack(submission, email_text, new_user, code):
    from_email = get_setting('from_address', 'email')

    context = {
        'base_url': get_setting('base_url', 'general'),
        'user': new_user,
        'code': code,
        'submission': submission,
    }

    email.send_email(
        get_setting(
            'new_user_subject',
            'email_subject',
            'New User : Profile Details'
        ),
        context,
        from_email,
        new_user.email,
        email_text,
        book=submission,
        kind='general',
    )


def handle_copyeditor_assignment(
        request,
        book,
        copyedit,
        files,
        due_date,
        note,
        email_text,
        requestor,
        attachment=None,
):
    new_copyeditor = models.CopyeditAssignment(
        book=book,
        copyeditor=copyedit,
        requestor=requestor,
        note=note,
        due=due_date,
    )
    new_copyeditor.save()

    new_copyeditor.files.add(*files)
    new_copyeditor.save()

    log.add_log_entry(
        book=book,
        user=requestor,
        kind='copyedit',
        message='Copyeditor %s %s assigned. Due %s' % (
            copyedit.first_name,
            copyedit.last_name,
            due_date,
        ),
        short_name='Copyedit Assignment',
    )
    send_copyedit_assignment(
        book,
        new_copyeditor,
        email_text,
        requestor,
        attachment=attachment,
    )


def handle_indexer_assignment(
        request,
        book,
        index,
        files,
        due_date,
        note,
        email_text,
        requestor,
        attachment,
):
    new_indexer = models.IndexAssignment(
        book=book,
        indexer=index,
        requestor=requestor,
        note=note,
        due=due_date,
    )

    new_indexer.save()
    [new_indexer.files.add(_file) for _file in files]
    new_indexer.save()
    send_invite_indexer(
        book,
        new_indexer,
        email_text,
        requestor,
        attachment,
    )

    log.add_log_entry(
        book=book,
        user=requestor,
        kind='index',
        message='Indexer %s %s assigned. Due %s' % (
            index.first_name, index.last_name, due_date
        ),
        short_name='Indexing Assignment',
    )


def handle_typeset_assignment(
        request,
        book,
        typesetter,
        files,
        due_date,
        email_text,
        requestor,
        attachment,
):
    new_typesetter = models.TypesetAssignment(
        book=book,
        typesetter=typesetter,
        requestor=requestor,
        due=due_date,
        note=email_text,
    )
    new_typesetter.save()

    new_typesetter.files.add(*files)
    new_typesetter.save()

    send_invite_typesetter(
        book,
        new_typesetter,
        email_text,
        requestor,
        attachment,
    )

    log.add_log_entry(
        book=book,
        user=requestor,
        kind='typeset',
        message='Typesetter %s %s assigned. Due %s' % (
            typesetter.first_name, typesetter.last_name,
            due_date), short_name='Typeset Assignment'
    )


def get_submission_tasks(book, user):
    task_list = []
    base_url = get_setting('base_url', 'general')

    copyedit_tasks = models.CopyeditAssignment.objects.filter(
        book=book,
        completed__isnull=False,
        editor_review__isnull=True,
        author_completed__isnull=True,
    )
    typeset_tasks = models.TypesetAssignment.objects.filter(
        (
            Q(completed__isnull=False) & Q(editor_review__isnull=True)
        ) | (
            Q(author_completed__isnull=False) &
            Q(editor_second_review__isnull=True)), book=book, requestor=user
    )

    for copyedit in copyedit_tasks:
        task_list.append({
            'type': 'copyedit', 'book': copyedit.book,
            'task': 'Copyedit Review', 'date': copyedit.completed,
            'title': copyedit.book.title,
            'url':
            'http://%s/editor/submission/%s/editing/view/copyeditor/%s/' % (
                base_url, copyedit.book.id, copyedit.id
            )
        })

    for typeset in typeset_tasks:
        task_list.append({
            'type': 'typeset', 'book': typeset.book,
            'task': 'Typesetting Review',
            'date': typeset.completed,
            'title': typeset.book.title,
            'url':
            'http://%s/editor/submission/%s/production/view/typesetter/%s' % (
                base_url, typeset.book.id, typeset.id
            )
        })

    return task_list


def create_new_review_round(book):
    latest_round = models.ReviewRound.objects.filter(book=book).aggregate(
        max=Max('round_number')
    )
    next_round = latest_round.get('max') + 1 if latest_round.get('max') > 0 \
        else 1
    return models.ReviewRound.objects.create(book=book, round_number=next_round)


def cancel_review_round(book):
    latest_round = models.ReviewRound.objects.filter(book=book).aggregate(
        max=Max('round_number')
    )
    cancel_round = models.ReviewRound.objects.get(
        book=book,
        round_number=latest_round.get('max')
    )
    cancel_round.delete()


def handle_review_assignment(
        request,
        book,
        reviewer,
        review_type,
        due_date,
        review_round,
        assigning_editor,
        email_text,
        review_form,
        attachment=None,
        access_key=None,
):
    obj, created = models.ReviewAssignment.objects.get_or_create(
        review_type=review_type,
        user=reviewer,
        assigning_editor=assigning_editor,
        book=book,
        review_round=review_round,
        defaults={
            'due': due_date,
            'review_form': review_form,
            'access_key': access_key,
        }
    )

    if created:
        book.review_assignments.add(obj)
        log.add_log_entry(
            book=book,
            user=assigning_editor,
            kind='review',
            message='Reviewer %s %s assigned. Round %d' % (
                reviewer.first_name,
                reviewer.last_name,
                review_round.round_number
            ),
            short_name='Review Assignment',
        )
        send_review_request(
            book=book,
            review_assignment=obj,
            email_text=email_text,
            sender=assigning_editor,
            attachment=attachment,
            access_key=access_key
        )
        return created
    else:
        messages.add_message(
            request,
            messages.WARNING,
            'Review Assignment for user <%s> already exists. '
            'User might already exist in one of the '
            'selected committees' % reviewer.username
        )
        return obj


def handle_editorial_review_assignment(
        request,
        book,
        editors,
        access_key,
        due_date,
        user,
        email_text,
        attachment=None,
):
    obj, created = models.EditorialReviewAssignment.objects.get_or_create(
        management_editor=user,
        completed=None,
        book=book,
        defaults={'due': due_date}
    )

    if obj.editorial_board_access_key:
        obj.publishing_committee_access_key = access_key
    else:
        obj.editorial_board_access_key = access_key

    obj.save()
    message = (
        "A new Editorial Review Assignment for %s has been "
        "assigned to you by %s ." % (
            book.title,
            request.user.username
        )
    )

    for editor in editors:
        if not obj.editorial_board.filter(username=editor.username).exists():
            notification = models.Task(
                assignee=editor,
                creator=request.user,
                text=message,
                workflow='editorial-review',
                editorial_review=obj,
                book=book,
            )
            notification.save()
            obj.editorial_board.add(editor)
            obj.save()
            log.add_log_entry(
                book=book,
                user=user,
                kind='review',
                message='Editorial member %s %s assigned.' % (
                    editor.first_name, editor.last_name
                ),
                short_name='Editorial Review Assignment',
            )

        else:
            messages.add_message(
                request,
                messages.WARNING,
                'Editorial Review Assignment for user <%s> already exists. '
                'User might already exist in one of the '
                'selected committees' % editor.username
            )

    if created:
        book.editorial_review_assignments.add(obj)
        send_editorial_review_request(book, obj, email_text, user, attachment)
        return obj
    return obj


# Email Handlers - TODO: move to email.py?

def send_review_request(
        book,
        review_assignment,
        email_text,
        sender,
        attachment=None,
        access_key=None,
):
    from_email = sender.email or get_setting('from_address', 'email')
    base_url = get_setting('base_url', 'general')
    press_name = get_setting('press_name', 'general')

    if access_key:
        decision_url = (
            'http://%s/review/%s/%s/assignment/%s/access_key/%s/decision/' % (
                base_url,
                review_assignment.review_type,
                book.id,
                review_assignment.id,
                access_key,
            )
        )
    else:
        decision_url = (
            'http://%s/review/%s/%s/assignment/%s/decision/' % (
                base_url,
                review_assignment.review_type,
                book.id,
                review_assignment.id
            )
        )

    context = {
        'book': book,
        'review': review_assignment,
        'decision_url': decision_url,
        'sender': sender,
        'base_url': base_url,
        'press_name': press_name,
    }

    email.send_email(
        subject=get_setting(
            'review_request_subject',
            'email_subject',
            'Review Request'
        ),
        context=context,
        from_email=from_email,
        to=review_assignment.user.email,
        html_template=email_text,
        book=book,
        attachment=attachment,
        kind='review',
        access_key=access_key,
    )


def send_editorial_review_request(
        book,
        review_assignment,
        email_text, sender,
        attachment=None
):
    from_email = sender.email or get_setting('from_address', 'email')
    base_url = get_setting('base_url', 'general')
    press_name = get_setting('press_name', 'general')

    if review_assignment.publishing_committee_access_key:
        decision_url = 'http://%s/editorial/submission/%s/access_key/%s/' % (
            base_url,
            book.id,
            review_assignment.publishing_committee_access_key,
        )
        access_key = review_assignment.publishing_committee_access_key
    else:
        decision_url = 'http://%s/editorial/submission/%s/access_key/%s/' % (
            base_url,
            book.id,
            review_assignment.editorial_board_access_key,
        )
        access_key = review_assignment.editorial_board_access_key

    context = {
        'book': book,
        'review': review_assignment,
        'decision_url': decision_url,
        'sender': sender,
        'base_url': base_url,
        'press_name': press_name,
    }

    for editor in review_assignment.editorial_board.all():
        email.send_email(
            get_setting(
                'editorial_review_request',
                'email_subject',
                'Editorial Review Request'
            ),
            context,
            from_email,
            editor.email,
            email_text,
            book=book,
            attachment=attachment,
            kind='review',
            access_key=access_key,
        )


def send_editorial_review_update(
        book,
        review_assignment,
        email_text,
        sender,
        attachment=None,
):
    from_email = sender.email or get_setting('from_address', 'email')

    context = {'book': book, 'review': review_assignment, 'sender': sender}

    for editor in review_assignment.editorial_board.all():
        email.send_email(
            get_setting(
                'editorial_review_due_date_subject',
                'email_subject',
                'Editorial Review Assignment {}: Due Date Updated'
            ) % review_assignment.id,
            context,
            from_email,
            editor.email,
            email_text,
            book=book,
            attachment=attachment,
            kind='review',
        )


def send_review_update(
        book,
        review_assignment,
        email_text,
        sender,
        attachment=None,
):
    """ Notify a reviewer that their review due date has been updated. """
    from_email = sender.email or get_setting('from_address', 'email')

    context = {'book': book, 'review': review_assignment, 'sender': sender}

    email.send_email(
        get_setting(
            'review_due_date_subject',
            'email_subject',
            'Review Assignment {}: Due Date Updated'.format(
                review_assignment.id
            )
        ),
        context,
        from_email,
        review_assignment.user.email,
        email_text,
        book=book,
        attachment=attachment,
        kind='review'
    )


def send_proposal_decline(proposal, email_text, sender):
    from_email = sender.email or get_setting('from_address', 'email')

    context = {'proposal': proposal, 'sender': sender}

    email.send_email(
        get_setting(
            'proposal_declined_subject',
            'email_subject',
            '[abp] Proposal Declined'
        ),
        context,
        from_email,
        proposal.owner.email,
        email_text,
        kind='proposal',
    )


def send_proposal_accept(
        proposal,
        email_text,
        submission,
        sender,
        attachment=None,
):
    from_email = sender.email or get_setting('from_address', 'email')

    context = {
        'base_url': get_setting('base_url', 'general'),
        'proposal': proposal,
        'submission': submission,
        'sender': sender,
    }

    email.send_email(
        get_setting(
            'proposal_accepted_subject',
            'email_subject',
            '[abp] Proposal Accepted'
        ),
        context,
        from_email,
        proposal.owner.email,
        email_text,
        book=submission,
        attachment=attachment,
    )


def send_proposal_revisions(proposal, email_text, sender):
    from_email = sender.email or get_setting('from_address', 'email')

    context = {
        'base_url': get_setting('base_url', 'general'),
        'proposal': proposal,
        'sender': sender,
    }

    email.send_email(
        get_setting(
            'proposal_revision_required_subject',
            'email_subject',
            '[abp] Proposal Revisions Required'
        ),
        context,
        from_email,
        proposal.owner.email,
        email_text,
        kind='proposal',
    )


def send_author_sign_off(submission, email_text, sender):
    from_email = sender.email or get_setting('from_address', 'email')

    context = {
        'base_url': get_setting('base_url', 'general'),
        'submission': submission,
        'sender': sender,
    }

    email.send_email(
        get_setting(
            'book_contract_uploaded_subject',
            'email_subject',
            'Book Contract Uploaded'
        ),
        context,
        from_email,
        submission.owner.email,
        email_text,
        book=submission,
        kind='submission',
    )


def send_copyedit_assignment(
        submission,
        copyedit,
        email_text,
        sender,
        attachment=None,
):
    from_email = sender.email or get_setting('from_address', 'email')

    context = {
        'base_url': get_setting('base_url', 'general'),
        'submission': submission,
        'copyedit': copyedit,
        'sender': sender,
    }

    email.send_email(
        get_setting(
            'copyedit_assignment_subject',
            'email_subject',
            'Copyedit Assignment'
        ),
        context,
        from_email,
        copyedit.copyeditor.email,
        email_text,
        book=submission,
        attachment=attachment,
        kind='copyedit',
    )


def send_author_invite(
        submission,
        copyedit,
        email_text,
        sender,
        attachment=None,
):
    from_email = sender.email or get_setting('from_address', 'email')

    context = {
        'base_url': get_setting('base_url', 'general'),
        'submission': submission,
        'copyedit': copyedit,
        'sender': sender,
    }

    email.send_email(
        get_setting(
            'copyediting_completed_subject',
            'email_subject',
            'Copyediting Completed'
        ),
        context,
        from_email,
        submission.owner.email,
        email_text,
        book=submission,
        attachment=attachment,
        kind='copyedit',
    )


def send_invite_indexer(book, index, email_text, sender, attachment=None):
    from_email = sender.email or get_setting('from_address', 'email')
    press_name = get_setting('press_name', 'general')

    context = {
        'base_url': get_setting('base_url', 'general'),
        'submission': book,
        'index': index,
        'sender': sender,
        'press_name': press_name,
    }

    email.send_email(
        get_setting(
            'indexing_request_subject',
            'email_subject',
            'Indexing Request'
        ),
        context,
        from_email,
        index.indexer.email,
        email_text,
        book=book,
        attachment=attachment,
        kind='index',
    )


def send_invite_typesetter(book, typeset, email_text, sender, attachment=None):
    from_email = sender.email or get_setting('from_address', 'email')

    context = {
        'base_url': get_setting('base_url', 'general'),
        'submission': typeset.book,
        'typeset': typeset,
        'sender': sender,
    }

    email.send_email(
        get_setting('typesetting_subject', 'email_subject', 'Typesetting'),
        context,
        from_email,
        typeset.typesetter.email,
        email_text,
        book=book,
        attachment=attachment,
        kind='typeset',
    )


def send_book_editors(book, added_editors, removed_editors, email_text):
    from_email = get_setting('from_address', 'email')
    base_url = get_setting('base_url', 'general')

    context = {
        'base_url': base_url,
        'submission': book,
        'added_editors': added_editors,
        'removed_editors': removed_editors,
        'submission_page': "http://%s/editor/submission/%s/" % (
            base_url,
            book.id,
        )
    }

    if added_editors or removed_editors:
        email.send_email(
            get_setting(
                'book_editors_subject',
                'email_subject',
                'Book Editors have been updated'
            ),
            context,
            from_email,
            book.owner.email,
            email_text,
            book=book,
            kind='general',
        )


def send_requests_revisions(
        book,
        sender,
        revision,
        email_text,
        attachments=None,
):
    from_email = sender.email or get_setting('from_address', 'email')
    base_url = get_setting('base_url', 'general')
    press_name = get_setting('press_name', 'general')

    context = {
        'book': book,
        'sender': sender,
        'revision': revision,
        'press_name': press_name,
        'revision_url': "http://%s/author/submission/%s/revisions/%s" % (
            base_url,
            book.id,
            revision.id,
        )
    }

    email.send_email_multiple(
        get_setting(
            'revisions_requested_subject',
            'email_subject',
            'Revisions Requested'
        ),
        context,
        from_email,
        book.owner.email,
        email_text,
        book=book,
        attachments=attachments,
        kind='revisions',
    )


def add_chapterauthors_from_author_models(chapter_id, authors):
    """ Populates `ChapterAuthors` from `Chapter.author`.

    Takes list of Author models tied to a Chapter through a ManyToMany
    relationship and saves ChapterAuthors based on those models if they don't
    already exist, then removes the author model from that chapter.
    """
    chapter = models.Chapter.objects.get(pk=chapter_id)
    count = 1

    for auth in authors:
        defaults = {
            'sequence': count,
            'first_name': smart_text(auth.first_name),
            'middle_name': smart_text(auth.middle_name),
            'last_name': smart_text(auth.last_name),
            'salutation': smart_text(auth.salutation),
            'institution': smart_text(auth.institution),
            'department': smart_text(auth.department),
            'country': smart_text(auth.country),
            'author_email': smart_text(auth.author_email),
            'biography': smart_text(auth.biography),
            'orcid': smart_text(auth.orcid),
            'twitter': smart_text(auth.twitter),
            'linkedin': smart_text(auth.linkedin),
            'facebook': smart_text(auth.facebook),
        }
        _, _ = models.ChapterAuthor.objects.get_or_create(
            chapter=chapter,
            old_author_id=auth.pk,
            defaults=defaults,
        )
        count += 1
        chapter.authors.remove(auth)
