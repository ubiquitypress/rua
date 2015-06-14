# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_remove_reviewassignment_form'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviewassignment',
            name='file',
        ),
        migrations.AddField(
            model_name='reviewassignment',
            name='files',
            field=models.ManyToManyField(to='core.File', null=True, blank=True),
        ),
    ]
