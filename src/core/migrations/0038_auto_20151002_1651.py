# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_auto_20151002_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='accepted',
            field=models.DateTimeField(default=False),
        ),
        migrations.AlterField(
            model_name='task',
            name='rejected',
            field=models.DateTimeField(default=False),
        ),
    ]
