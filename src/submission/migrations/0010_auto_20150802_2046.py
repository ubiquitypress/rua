# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0009_proposal_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='status',
            field=models.CharField(default=b'submission', max_length=20, choices=[(b'submission', b'Submission'), (b'revisions_required', b'Revisions Required'), (b'revisions_submitted', b'Revisions Submitted'), (b'accepted', b'Accepted'), (b'declined', b'Declined')]),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='uploaded_file',
            field=models.FileField(null=True, upload_to=b'', blank=True),
        ),
    ]
