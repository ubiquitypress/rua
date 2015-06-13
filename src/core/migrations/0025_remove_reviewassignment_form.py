# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_auto_20150613_1124'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviewassignment',
            name='form',
        ),
    ]
