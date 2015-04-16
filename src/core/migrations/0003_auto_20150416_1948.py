# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150416_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='stage_uploaded',
            field=models.IntegerField(),
            preserve_default=True,
        ),
    ]
