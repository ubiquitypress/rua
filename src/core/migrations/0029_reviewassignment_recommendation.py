# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_auto_20150614_1847'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewassignment',
            name='recommendation',
            field=models.CharField(blank=True, max_length=10, null=True, choices=[(b'accept', b'Accept'), (b'reject', b'Reject')]),
        ),
    ]
