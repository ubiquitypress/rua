# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0094_auto_20160308_1326'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='emailed',
            field=models.BooleanField(default=False),
        ),
    ]
