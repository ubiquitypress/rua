# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0006_auto_20150708_2016'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='date_submitted',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 9, 16, 11, 35, 728391, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
