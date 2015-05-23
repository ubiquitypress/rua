# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20150522_2337'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='sequence',
            field=models.IntegerField(default=1),
        ),
    ]
