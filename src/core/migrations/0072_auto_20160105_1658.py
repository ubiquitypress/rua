# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0071_auto_20160105_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='proposal',
            field=models.ForeignKey(related_name='proposal_log', blank=True, to='core.Book', null=True),
        ),
        migrations.AlterField(
            model_name='log',
            name='kind',
            field=models.CharField(max_length=100, choices=[(b'submission', b'Submission'), (b'workflow', b'Workflow'), (b'file', b'File'), (b'copyedit', b'Copyedit'), (b'review', b'Review'), (b'index', b'Index'), (b'typeset', b'Typeset'), (b'revisions', b'Revisions'), (b'editing', b'Editing'), (b'production', b'Production'), (b'proposal', b'Proposal')]),
        ),
    ]
