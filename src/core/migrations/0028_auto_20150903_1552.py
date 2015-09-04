# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_auto_20150902_1432'),
    ]

    operations = [
        migrations.AddField(
            model_name='typesetassignment',
            name='editor_second_review',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='typesetassignment',
            name='note_from_typesetter',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='typesetassignment',
            name='typesetter_files',
            field=models.ManyToManyField(related_name='typsetter_files', null=True, to='core.File', blank=True),
        ),
        migrations.AddField(
            model_name='typesetassignment',
            name='typsetter_completed',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='typesetassignment',
            name='typsetter_invited',
            field=models.DateField(null=True, blank=True),
        ),
    ]
