# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150521_1950'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='book_type',
            field=models.CharField(default='', max_length=50, choices=[(b'monograph', b'Monograph'), (b'edited_volume', b'Edited Volume')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='prefix',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
