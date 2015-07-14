# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0008_auto_20150709_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='status',
            field=models.CharField(default='submission', max_length=20, choices=[(b'submission', b'Submission'), (b'revisions_required', b'Revisions Required'), (b'accepted', b'Accepted'), (b'declined', b'Declined')]),
            preserve_default=False,
        ),
    ]
