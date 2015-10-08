# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0046_auto_20151008_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='date_updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 8, 11, 53, 20, 111180, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='file',
            name='date_uploaded',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 8, 11, 52, 57, 996159, tzinfo=utc)),
        ),
    ]
