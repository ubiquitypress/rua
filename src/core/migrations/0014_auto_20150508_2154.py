# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_book_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stage',
            name='current_stage',
            field=models.CharField(blank=True, max_length=b'20', null=True, choices=[(b'proposal', b'Proposal'), (b'submission', b'Submission'), (b'i_review', b'Internal Review'), (b'e_review', b'External Review'), (b'copy_editing', b'Copy Editing'), (b'indexing', b'Indexing'), (b'production', b'Production'), (b'published', b'Published')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='workflow',
            field=models.CharField(max_length=50, choices=[(b'submission', b'Submission'), (b'review', b'Review'), (b'editing', b'Editing'), (b'production', b'Production'), (b'personal', b'Personal')]),
            preserve_default=True,
        ),
    ]
