# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_copyeditassignment_author_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='copyeditassignment',
            name='author_files',
            field=models.ManyToManyField(related_name='author_copyedit_files', null=True, to='core.File', blank=True),
        ),
        migrations.AddField(
            model_name='copyeditassignment',
            name='note_from_author',
            field=models.TextField(null=True, blank=True),
        ),
    ]
