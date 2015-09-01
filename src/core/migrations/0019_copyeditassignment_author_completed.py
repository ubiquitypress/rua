# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_copyeditassignment_note_to_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='copyeditassignment',
            name='author_completed',
            field=models.DateField(null=True, blank=True),
        ),
    ]
