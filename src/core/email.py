from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context, Template

from core import models
from core import log

from pprint import pprint

def send_email(subject, context, from_email, to, html_template, book=None):

    htmly = Template(html_template)
    con = Context(context)
    html_content = htmly.render(con)

    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    if book:
    	log.add_email_log_entry(book, subject, from_email, to, html_content)
