# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0069_indexassignment_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='copyeditassignment',
            name='note_from_copyeditor',
            field=models.TextField(null=True, blank=True),
        ),
    ]
