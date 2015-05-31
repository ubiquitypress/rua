# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20150531_1811'),
    ]

    operations = [
        migrations.AddField(
            model_name='license',
            name='version',
            field=models.CharField(default='1.0', max_length=10),
            preserve_default=False,
        ),
    ]
