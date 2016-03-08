# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cron', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crontask',
            name='schedule',
            field=models.CharField(max_length=20, choices=[(b'hourly', b'Hourly'), (b'daily', b'Daily'), (b'weekly', b'Weekly')]),
        ),
    ]
