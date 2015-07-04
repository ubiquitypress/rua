# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_auto_20150614_2252'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='setting',
            options={'ordering': ('group', 'name')},
        ),
        migrations.RenameField(
            model_name='stage',
            old_name='copy_editing',
            new_name='editing',
        ),
        migrations.RemoveField(
            model_name='stage',
            name='indexing',
        ),
        migrations.AlterField(
            model_name='stage',
            name='current_stage',
            field=models.CharField(blank=True, max_length=b'20', null=True, choices=[(b'proposal', b'Proposal'), (b'submission', b'New Submission'), (b'i_review', b'Internal Review'), (b'e_review', b'External Review'), (b'editing', b'Editing'), (b'production', b'Production'), (b'published', b'Published'), (b'declined', b'Declined')]),
        ),
    ]
