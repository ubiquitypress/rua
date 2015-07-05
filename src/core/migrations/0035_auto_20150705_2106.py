# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_chapter'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='sequence',
            field=models.IntegerField(default=9999),
        ),
        migrations.AddField(
            model_name='format',
            name='sequence',
            field=models.IntegerField(default=9999),
        ),
    ]
