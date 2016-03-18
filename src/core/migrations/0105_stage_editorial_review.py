# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0104_auto_20160317_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='stage',
            name='editorial_review',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
