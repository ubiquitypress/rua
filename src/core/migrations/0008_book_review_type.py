# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20150828_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='review_type',
            field=models.CharField(default=b'closed', max_length=50, choices=[(b'closed', b'Closed'), (b'open-with', b'Open with Reviewer Info'), (b'open-without', b'Open without Reviewer Info')]),
        ),
    ]
