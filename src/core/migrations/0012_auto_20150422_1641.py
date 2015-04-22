# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_stage_current_stage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stage',
            name='book',
        ),
        migrations.AddField(
            model_name='book',
            name='stage',
            field=models.ForeignKey(blank=True, to='core.Stage', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='book',
            name='cover',
            field=models.ImageField(null=True, upload_to=b'', blank=True),
            preserve_default=True,
        ),
    ]
