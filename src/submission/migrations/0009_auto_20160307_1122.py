# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0008_auto_20160304_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposalreview',
            name='blind',
            field=models.NullBooleanField(default=False),
        ),
    ]
