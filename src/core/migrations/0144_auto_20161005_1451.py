# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0143_auto_20161004_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settinggroup',
            name='id',
            field=models.CharField(max_length=20, serialize=False, primary_key=True),
        ),
    ]
