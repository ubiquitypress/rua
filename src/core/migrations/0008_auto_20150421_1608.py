# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_task_workflow'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='assigned',
            field=models.DateField(auto_now_add=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='due',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
