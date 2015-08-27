from core import models
from core import email

def send_requests_revisions(book, revision, email_text):
    from_email = models.Setting.objects.get(group__name='email', name='from_address')
    base_url = models.Setting.objects.get(group__name='general', name='base_url').value

    context = {
        'book': book,
        'revision': revision,
        'revision_url': "http://%s/revisions/%s" % (base_url, revision.id)
    }

    email.send_email('Revisions Requested', context, from_email.value, book.owner.email, email_text)