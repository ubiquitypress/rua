# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0005_proposal_revision_due_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='date_accepted',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
