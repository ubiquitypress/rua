# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0005_auto_20160120_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formelementsrelationship',
            name='width',
            field=models.CharField(default=datetime.datetime(2016, 1, 20, 16, 40, 46, 974101, tzinfo=utc), max_length=20, choices=[(b'col-md-4', b'third'), (b'col-md-6', b'half'), (b'col-md-12', b'full')]),
            preserve_default=False,
        ),
    ]
