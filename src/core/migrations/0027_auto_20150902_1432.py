# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_auto_20150902_1327'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='typesetassignment',
            name='index_files',
        ),
        migrations.AddField(
            model_name='indexassignment',
            name='index_files',
            field=models.ManyToManyField(related_name='index_files', null=True, to='core.File', blank=True),
        ),
    ]
