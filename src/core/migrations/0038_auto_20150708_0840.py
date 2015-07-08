# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_auto_20150705_2159'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chapter',
            options={'ordering': ('sequence', 'name')},
        ),
        migrations.AlterModelOptions(
            name='format',
            options={'ordering': ('sequence', 'name')},
        ),
        migrations.AddField(
            model_name='stage',
            name='review',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='stage',
            name='current_stage',
            field=models.CharField(blank=True, max_length=b'20', null=True, choices=[(b'proposal', b'Proposal'), (b'submission', b'New Submission'), (b'review', b'Review'), (b'editing', b'Editing'), (b'production', b'Production'), (b'published', b'Published'), (b'declined', b'Declined')]),
        ),
    ]
