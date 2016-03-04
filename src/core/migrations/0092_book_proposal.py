# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0005_proposal_revision_due_date'),
        ('core', '0091_reviewassignment_reopened'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='proposal',
            field=models.ForeignKey(blank=True, to='submission.Proposal', null=True),
        ),
    ]
