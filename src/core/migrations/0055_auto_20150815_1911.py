# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0054_auto_20150815_1856'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chapter',
            old_name='indentifier',
            new_name='identifier',
        ),
    ]
