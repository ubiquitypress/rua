# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0059_auto_20151026_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='workflow',
            field=models.CharField(blank=True, max_length=50, null=True, choices=[(b'submission', b'Submission'), (b'review', b'Review'), (b'editing', b'Editing'), (b'production', b'Production'), (b'personal', b'Personal')]),
        ),
    ]
