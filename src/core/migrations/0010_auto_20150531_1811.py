# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20150523_1502'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ('sequence',)},
        ),
        migrations.AlterModelOptions(
            name='editor',
            options={'ordering': ('sequence',)},
        ),
    ]
