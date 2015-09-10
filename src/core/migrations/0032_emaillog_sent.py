# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_emaillog'),
    ]

    operations = [
        migrations.AddField(
            model_name='emaillog',
            name='sent',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 10, 17, 50, 47, 189361, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
