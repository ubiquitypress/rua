# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_emaillog_sent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='kind',
            field=models.CharField(max_length=100, choices=[(b'submission', b'Submission'), (b'workflow', b'Workflow'), (b'file', b'File'), (b'copyedit', b'Copyedit'), (b'review', b'Review'), (b'index', b'Index'), (b'typeset', b'Typeset'), (b'revisions', b'Revisions'), (b'editing', b'Editing'), (b'production', b'Production')]),
        ),
    ]
