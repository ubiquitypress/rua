# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150521_1908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover_letter',
            field=models.TextField(null=True, blank=True),
        ),
    ]
