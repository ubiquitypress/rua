from core import models as core_models
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

def check_stage(book_stage, check):
    if book_stage >= check:
        pass
    else:
        raise PermissionDenied()
