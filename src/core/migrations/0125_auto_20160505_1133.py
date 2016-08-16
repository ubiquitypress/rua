# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from core import models as core_models

def load_setting(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    setting_group, created = core_models.SettingGroup.objects.get_or_create(name='email', enabled=True)
    content = "<p>Dear  {% if receiver %}{{receiver.profile.full_name}}{%else%}[NAME]{%endif%},</p>\r\n\r\n<p>The book proposal, {{proposal.title}} {% if proposal.subtitle %}: {{proposal.subtitle}} {% endif %}, that is in process with {{press_name}} has been transferred into your name. This means that you are now the corresponding author/editor during the processing of this proposal. We will use this contact address to correspond with you regarding the review of the proposal and the ultimate editorial decision. We will be in touch once the next stages are complete.</p>\r\n\r\n<p>As the corresponding author you will now be able to log into the book management system to view the proposal details, submit revisions and correspond with the assigned Book Editor. The proposal can be access via the below link (you should already have login details:</p>\r\n\r\n<p>{{base_url}}{{proposal_url}}</p>\r\n\r\n<p>Should you have received this email in error, please let us know as soon as possible.</p>\r\n\r\n<p>Kind regards,</p>\r\n<p>{{sender.username}}</p>\r\n<p>{{sender.profile.signature}}</p>"
    description = "Email sent when changing proposal owner/principal contact"
    setting = core_models.Setting.objects.get_or_create(name='change_principal_contact_proposal', group=setting_group, types ='rich_text', defaults={ 'value' : content, 'description' : description })

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0124_auto_20160504_1323'),
    ]

    operations = [
        migrations.RunPython(load_setting),
    ]
