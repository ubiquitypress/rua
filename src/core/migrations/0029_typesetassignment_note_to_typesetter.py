# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_auto_20150903_1552'),
    ]

    operations = [
        migrations.AddField(
            model_name='typesetassignment',
            name='note_to_typesetter',
            field=models.TextField(null=True, blank=True),
        ),
    ]
