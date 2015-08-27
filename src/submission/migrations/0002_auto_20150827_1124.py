# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='author',
            field=models.CharField(default='author', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='proposal',
            name='subtitle',
            field=models.CharField(default='title', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='proposal',
            name='title',
            field=models.CharField(default='subtitle', max_length=255),
            preserve_default=False,
        ),
    ]
