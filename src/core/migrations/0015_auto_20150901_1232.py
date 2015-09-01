# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20150831_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='copyeditassignment',
            name='copyedit_files',
            field=models.ForeignKey(related_name='copyedit_files', blank=True, to='core.File', null=True),
        ),
        migrations.AddField(
            model_name='copyeditassignment',
            name='note',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='copyeditassignment',
            name='files',
            field=models.ManyToManyField(related_name='cp_assigned_files', null=True, to='core.File', blank=True),
        ),
    ]
