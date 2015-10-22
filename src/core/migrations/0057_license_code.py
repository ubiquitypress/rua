# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0056_auto_20151021_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='license',
            name='code',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
