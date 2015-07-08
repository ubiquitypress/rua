# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0040_auto_20150708_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='reviewer_suggestions',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='reviewassignment',
            name='recommendation',
            field=models.CharField(blank=True, max_length=10, null=True, choices=[(b'accept', b'Accept'), (b'reject', b'Reject'), (b'revisions_required', b'Revisions Required')]),
        ),
    ]
