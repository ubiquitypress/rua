# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_squashed_0017_log_short_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='short_name',
            field=models.CharField(max_length=100),
        ),
    ]
