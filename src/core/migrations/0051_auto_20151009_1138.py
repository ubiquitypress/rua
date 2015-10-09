# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0050_auto_20151009_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emaillog',
            name='bcc',
            field=models.EmailField(max_length=1000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='emaillog',
            name='cc',
            field=models.EmailField(max_length=1000, null=True, blank=True),
        ),
    ]
