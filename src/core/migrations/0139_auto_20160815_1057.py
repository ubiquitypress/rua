# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0138_book_publisher_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='publisher_location',
            field=models.CharField(help_text=b'If not default press location.', max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='publisher_name',
            field=models.CharField(help_text=b'If not default press name.', max_length=100, null=True, blank=True),
        ),
    ]
