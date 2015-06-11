from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context, Template

from core import models

from pprint import pprint

def send_email(subject, context, from_email, to, html_template):

    htmly = Template(html_template)
    con = Context(context)
    html_content = htmly.render(con)

    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
