# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0029_auto_20160802_1012'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposalreview',
            name='access_key',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
