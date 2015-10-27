# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0060_auto_20151026_1645'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='role',
            options={'ordering': ('sequence', 'name')},
        ),
        migrations.AddField(
            model_name='role',
            name='required',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='role',
            name='sequence',
            field=models.IntegerField(default=999),
        ),
    ]
