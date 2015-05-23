# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_author_sequence'),
    ]

    operations = [
        migrations.AddField(
            model_name='editor',
            name='sequence',
            field=models.IntegerField(default=1, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='sequence',
            field=models.IntegerField(default=1, null=True, blank=True),
        ),
    ]
