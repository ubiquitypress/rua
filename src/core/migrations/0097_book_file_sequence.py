# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0096_auto_20160315_1122'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='file_sequence',
            field=models.IntegerField(default=1),
        ),
    ]
