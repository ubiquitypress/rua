# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0072_auto_20160107_1017'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='primary_contact',
            field=models.BooleanField(default=False),
        ),
    ]
