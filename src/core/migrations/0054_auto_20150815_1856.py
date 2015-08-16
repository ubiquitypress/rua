# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0053_auto_20150809_1120'),
    ]

    operations = [
        migrations.RenameField(
            model_name='format',
            old_name='indentifier',
            new_name='identifier',
        ),
    ]
