# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_auto_20150705_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='indentifier',
            field=models.CharField(unique=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='format',
            name='indentifier',
            field=models.CharField(unique=True, max_length=200),
        ),
    ]
