# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from core import models as core_models

def load_setting(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    content = "Dear _receiver_ ,\r\n<p>You have been assigned as a book editor of this proposal {{proposal.title}} {% if proposal.subtitle %}: {{proposal.subtitle}}{% endif %}<proposal id:{{proposal.id}}=\"\"> has been updated.</proposal></span></p>\r\n<p>These are all the book editors assigned to the proposal: </p>\r\n--------\r\n_proposal_editors_\r\n----------\r\n\r\n</p><p> \r\nTo view the proposal, use the following link: http://{{base_url}}/proposals/{{proposal.id}}/\r\n<br></p><p><span style=\"line-height: 1.42857;\">Regards,\r\n<br><br>RUA notification system</span><br></p><p></p>"  
    description = "Email sent to editors when they are assigned to a proposal."
    setting = core_models.Setting.objects.get_or_create(name='book_editor_proposal_ack', group=core_models.SettingGroup.objects.get(name='email'), types ='rich_text', defaults={ 'value' : content, 'description' : description })    
    setting_subject = core_models.Setting.objects.get_or_create(name='proposal_book_editors_subject', group=core_models.SettingGroup.objects.get(name='email_subject'), types ='text', defaults={ 'value' : 'Proposal Book Editors: Update', 'description' : "Email subject. Do not remove '%s' or other string format related parts." })


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0126_auto_20160505_1228'),
    ]

    operations = [
        migrations.RunPython(load_setting),
    ]
