# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0051_auto_20151009_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='sequence',
            field=models.IntegerField(default=999),
        ),
    ]
