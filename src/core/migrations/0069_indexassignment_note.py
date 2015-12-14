# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0068_indexassignment_note_to_indexer'),
    ]

    operations = [
        migrations.AddField(
            model_name='indexassignment',
            name='note',
            field=models.TextField(null=True, blank=True),
        ),
    ]
