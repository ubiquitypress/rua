# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20150901_1232'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='copyeditassignment',
            name='copyedit_files',
        ),
        migrations.AddField(
            model_name='copyeditassignment',
            name='copyedit_files',
            field=models.ManyToManyField(related_name='copyedit_files', null=True, to='core.File', blank=True),
        ),
    ]
