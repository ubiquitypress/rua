# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0043_reviewassignment_competing_interests'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewassignment',
            name='competing_interests',
            field=models.TextField(help_text=b"If any of the authors or editors have any competing interests please add them here. EG. 'This study was paid for by corp xyz.'", null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='reviewassignment',
            name='recommendation',
            field=models.CharField(blank=True, max_length=10, null=True, choices=[(b'accept', b'Accept'), (b'reject', b'Reject'), (b'revisions', b'Revisions Required')]),
        ),
    ]
