# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0002_auto_20150416_2041'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='funding',
            field=models.TextField(max_length=500, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='proposal',
            name='subtitle',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
