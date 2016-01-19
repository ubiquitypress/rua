# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0087_auto_20160118_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
    ]
