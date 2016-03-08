# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0010_auto_20160308_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='author',
            field=models.CharField(max_length=255, verbose_name=b'Submitting author/editor'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='title',
            field=models.CharField(max_length=255, verbose_name=b'Book Title'),
        ),
    ]
