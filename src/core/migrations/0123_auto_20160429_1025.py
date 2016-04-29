# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0122_auto_20160429_1018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emaillog',
            name='kind',
            field=models.CharField(default=b'general', max_length=100, choices=[(b'submission', b'Submission'), (b'workflow', b'Workflow'), (b'file', b'File'), (b'copyedit', b'Copyedit'), (b'review', b'Review'), (b'proposal_review', b'Proposal Review'), (b'index', b'Index'), (b'typeset', b'Typeset'), (b'revisions', b'Revisions'), (b'editing', b'Editing'), (b'production', b'Production'), (b'proposal', b'Proposal'), (b'general', b'General'), (b'reminder', b'Reminder')]),
        ),
    ]
