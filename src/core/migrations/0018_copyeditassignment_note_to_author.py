# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20150901_1852'),
    ]

    operations = [
        migrations.AddField(
            model_name='copyeditassignment',
            name='note_to_author',
            field=models.TextField(null=True, blank=True),
        ),
    ]
