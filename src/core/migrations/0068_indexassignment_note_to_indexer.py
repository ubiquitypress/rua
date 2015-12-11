# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0067_auto_20151209_1329'),
    ]

    operations = [
        migrations.AddField(
            model_name='indexassignment',
            name='note_to_indexer',
            field=models.TextField(null=True, blank=True),
        ),
    ]
