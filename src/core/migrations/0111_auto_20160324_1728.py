# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0110_apiconnector'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apiconnector',
            name='slug',
            field=models.CharField(default=datetime.datetime(2016, 3, 24, 17, 28, 47, 409835, tzinfo=utc), unique=True, max_length=1000),
            preserve_default=False,
        ),
    ]
