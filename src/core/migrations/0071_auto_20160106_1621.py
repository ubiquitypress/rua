# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0003_proposal_requestor'),
        ('core', '0070_copyeditassignment_note_from_copyeditor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='book',
            field=models.ForeignKey(blank=True, to='core.Book', null=True),
        ),
        migrations.AddField(
            model_name='emaillog',
            name='attachment',
            field=models.ManyToManyField(related_name='email_attachment', null=True, to='core.File', blank=True),
        ),
        migrations.AddField(
            model_name='log',
            name='proposal',
            field=models.ForeignKey(related_name='proposal_log', blank=True, to='submission.Proposal', null=True),
        ),
        migrations.AlterField(
            model_name='log',
            name='kind',
            field=models.CharField(max_length=100, choices=[(b'submission', b'Submission'), (b'workflow', b'Workflow'), (b'file', b'File'), (b'copyedit', b'Copyedit'), (b'review', b'Review'), (b'index', b'Index'), (b'typeset', b'Typeset'), (b'revisions', b'Revisions'), (b'editing', b'Editing'), (b'production', b'Production'), (b'proposal', b'Proposal')]),
        ),
    ]
