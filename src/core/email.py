from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context, Template
from django.conf import settings

from core import models
from core import log

from pprint import pprint

def filepath(book, attachment):
	return '%s/%s/%s' % (settings.BOOK_DIR, book.id, attachment.uuid_filename)

def filepath_proposal(proposal, attachment):
	return '%s/%s/%s' % (settings.PROPOSAL_DIR, proposal.id, attachment.uuid_filename)

def send_email(subject, context, from_email, to, html_template, bcc=None, cc=None, book=None, attachment=None, proposal=None):

	html_template.replace('\n', '<br />')

	htmly = Template(html_template)
	con = Context(context)
	html_content = htmly.render(con)

	if not type(to) in [list,tuple]:
		to = [to]

	msg = EmailMultiAlternatives(subject, html_content, from_email, to, bcc=bcc, cc=cc)
	
	if book:
		log.add_email_log_entry(book = book, subject = subject, from_address = from_email, to = to, bcc = bcc, cc = cc, content = html_content, attachment = attachment)
	if proposal:
		log.add_email_log_entry(proposal = proposal, subject = subject, from_address = from_email, to = to, bcc = bcc, cc = cc, content = html_content, attachment = attachment)
		
	msg.content_subtype = "html"

	if attachment:
		if book:
			msg.attach_file(filepath(book, attachment))
		else:
			msg.attach_file(filepath_proposal(proposal, attachment))

	msg.send()

