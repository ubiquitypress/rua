# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0020_historyproposal_date_edited'),
    ]

    operations = [
        migrations.AddField(
            model_name='historyproposal',
            name='version',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='proposal',
            name='current_version',
            field=models.IntegerField(default=1),
        ),
    ]
