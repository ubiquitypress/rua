# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0003_auto_20150611_2039'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formresult',
            name='status',
        ),
    ]
