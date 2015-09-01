# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20150901_1238'),
    ]

    operations = [
        migrations.AddField(
            model_name='copyeditassignment',
            name='author_invited',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='copyeditassignment',
            name='editor_review',
            field=models.DateField(null=True, blank=True),
        ),
    ]
