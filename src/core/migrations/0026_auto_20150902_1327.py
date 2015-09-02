# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_auto_20150902_1312'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='indexassignment',
            name='author_files',
        ),
        migrations.RemoveField(
            model_name='indexassignment',
            name='index_files',
        ),
        migrations.RemoveField(
            model_name='indexassignment',
            name='typeset_files',
        ),
        migrations.AddField(
            model_name='typesetassignment',
            name='author_completed',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='typesetassignment',
            name='author_files',
            field=models.ManyToManyField(related_name='author_typeset_files', null=True, to='core.File', blank=True),
        ),
        migrations.AddField(
            model_name='typesetassignment',
            name='author_invited',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='typesetassignment',
            name='editor_review',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='typesetassignment',
            name='index_files',
            field=models.ManyToManyField(related_name='index_files', null=True, to='core.File', blank=True),
        ),
        migrations.AddField(
            model_name='typesetassignment',
            name='note',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='typesetassignment',
            name='note_from_author',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='typesetassignment',
            name='note_to_author',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='typesetassignment',
            name='typeset_files',
            field=models.ManyToManyField(related_name='typeset_files', null=True, to='core.File', blank=True),
        ),
    ]
