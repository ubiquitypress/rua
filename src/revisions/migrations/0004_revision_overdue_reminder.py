# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('revisions', '0003_revision_requestor'),
    ]

    operations = [
        migrations.AddField(
            model_name='revision',
            name='overdue_reminder',
            field=models.BooleanField(default=False),
        ),
    ]
