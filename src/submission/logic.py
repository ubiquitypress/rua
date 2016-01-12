from core import models as core_models
from core import email
from django.core.exceptions import PermissionDenied

def copy_author_to_submission(user, book):
    author = core_models.Author(
        first_name = user.first_name,
        middle_name = user.profile.middle_name,
        last_name = user.last_name,
        salutation = user.profile.salutation,
        institution = user.profile.institution,
        department = user.profile.department,
        country = user.profile.country,
        author_email = user.email,
        biography = user.profile.biography,
        orcid = user.profile.orcid,
        twitter = user.profile.twitter,
        linkedin = user.profile.linkedin,
        facebook = user.profile.facebook,
    )

    author.save()
    book.author.add(author)
    return author

def copy_editor_to_submission(user, book):
    editor = core_models.Editor(
        first_name = user.first_name,
        middle_name = user.profile.middle_name,
        last_name = user.last_name,
        salutation = user.profile.salutation,
        institution = user.profile.institution,
        department = user.profile.department,
        country = user.profile.country,
        author_email = user.email,
        biography = user.profile.biography,
        orcid = user.profile.orcid,
        twitter = user.profile.twitter,
        linkedin = user.profile.linkedin,
        facebook = user.profile.facebook,
    )

    editor.save()
    book.editor.add(editor)
    return editor

def check_stage(book, check):
    if book.submission_stage >= check:
        pass
    elif book.submission_date:
        raise PermissionDenied()
    else:
        raise PermissionDenied()

def send_acknowldgement_email(book, press_editors):
    from_email = core_models.Setting.objects.get(group__name='email', name='from_address').value
    author_text = core_models.Setting.objects.get(group__name='email', name='author_submission_ack').value
    editor_text = core_models.Setting.objects.get(group__name='email', name='editor_submission_ack').value
    press_name = core_models.Setting.objects.get(group__name='general', name='press_name').value

    context = {
        'base_url': core_models.Setting.objects.get(group__name='general', name='base_url').value,
        'submission': book,
        'press_name':press_name,
        'principal_contact_name':'principal_contact_name',
    }

    email.send_email('Submission Acknowledgement', context, from_email, book.owner.email, author_text, book=book)

    for editor in press_editors:
        email.send_email('New Submission', context, from_email, editor.email, editor_text, book=book) 

def handle_book_labels(post, book, kind):
    for _file in book.files.all():
        if _file.kind == kind and  post.get("%s" % _file.id, None):
            _file.label = post.get("%s" % _file.id)
            _file.save()

