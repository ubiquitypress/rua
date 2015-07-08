# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_auto_20150708_0840'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='review_files',
        ),
        migrations.AddField(
            model_name='book',
            name='external_review_files',
            field=models.ManyToManyField(related_name='external_review_files', null=True, to='core.File', blank=True),
        ),
        migrations.AddField(
            model_name='book',
            name='internal_review_files',
            field=models.ManyToManyField(related_name='internal_review_files', null=True, to='core.File', blank=True),
        ),
    ]
