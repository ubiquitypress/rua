# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0047_auto_20151008_1153'),
    ]

    operations = [
        migrations.RenameField(
            model_name='file',
            old_name='date_updated',
            new_name='date_modified',
        ),
        migrations.AlterField(
            model_name='file',
            name='date_uploaded',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 8, 11, 55, 55, 106733, tzinfo=utc)),
        ),
    ]
