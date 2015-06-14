# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_reviewassignment_declined'),
    ]

    operations = [
        migrations.AddField(
            model_name='stage',
            name='declined',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='stage',
            name='current_stage',
            field=models.CharField(blank=True, max_length=b'20', null=True, choices=[(b'proposal', b'Proposal'), (b'submission', b'New Submission'), (b'i_review', b'Internal Review'), (b'e_review', b'External Review'), (b'copy_editing', b'Copy Editing'), (b'indexing', b'Indexing'), (b'production', b'Production'), (b'published', b'Published'), (b'declined', b'Declined')]),
        ),
    ]
