# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0107_auto_20160318_1046'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='editorial_review',
            field=models.ForeignKey(blank=True, to='core.EditorialReviewAssignment', null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='workflow',
            field=models.CharField(blank=True, max_length=50, null=True, choices=[(b'submission', b'Submission'), (b'review', b'Review'), (b'editorial-review', b'Editorial Review'), (b'editing', b'Editing'), (b'production', b'Production'), (b'personal', b'Personal'), (b'proposal', b'Proposal')]),
        ),
    ]
