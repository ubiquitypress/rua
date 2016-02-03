# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0004_auto_20160129_1547'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='revision_due_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
