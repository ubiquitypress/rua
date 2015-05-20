# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='short_name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
