# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='workflow',
            field=models.CharField(default='submission', max_length=50),
            preserve_default=False,
        ),
    ]
