# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_auto_20150902_1214'),
    ]

    operations = [
        migrations.AddField(
            model_name='indexassignment',
            name='author_files',
            field=models.ManyToManyField(related_name='author_typeset_files', null=True, to='core.File', blank=True),
        ),
        migrations.AddField(
            model_name='indexassignment',
            name='typeset_files',
            field=models.ManyToManyField(related_name='typeset_files', null=True, to='core.File', blank=True),
        ),
    ]
