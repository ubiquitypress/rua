# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_book_languages'),
    ]

    operations = [
        migrations.AddField(
            model_name='stage',
            name='copyediting',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='stage',
            name='indexing',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='stage',
            name='typesetting',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='languages',
            field=models.ManyToManyField(to='core.Language', null=True, blank=True),
        ),
    ]
