# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0053_auto_20150809_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='name',
            field=models.CharField(unique=True, max_length=100),
        ),
    ]
