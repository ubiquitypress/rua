# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_auto_20150705_2106'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='name',
            field=models.CharField(default=' ', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='format',
            name='name',
            field=models.CharField(default=' ', max_length=200),
            preserve_default=False,
        ),
    ]
