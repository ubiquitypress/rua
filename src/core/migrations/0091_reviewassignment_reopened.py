# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0090_auto_20160304_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewassignment',
            name='reopened',
            field=models.BooleanField(default=False),
        ),
    ]
