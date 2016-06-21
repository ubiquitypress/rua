# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from core import models as core_models

def load_setting(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    setting_group, created = core_models.SettingGroup.objects.get_or_create(name='email_subject', defaults={'enabled': True})
    setting_subject = core_models.Setting.objects.get_or_create(name='change_principal_contact_proposal_subject', group=setting_group, types ='text', defaults={ 'value' : 'Proposal Owner Change', 'description' : "Email subject. Do not remove '%s' or other string format related parts." })


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0125_auto_20160505_1133'),
    ]

    operations = [
        migrations.RunPython(load_setting),
    ]