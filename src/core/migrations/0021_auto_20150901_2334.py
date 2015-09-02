# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20150901_2212'),
    ]

    operations = [
        migrations.AddField(
            model_name='indexassignment',
            name='index_files',
            field=models.ManyToManyField(related_name='index_files', null=True, to='core.File', blank=True),
        ),
        migrations.AddField(
            model_name='indexassignment',
            name='note_from_indexer',
            field=models.TextField(null=True, blank=True),
        ),
    ]
