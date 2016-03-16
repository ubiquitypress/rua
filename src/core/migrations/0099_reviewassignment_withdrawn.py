# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0098_remove_book_file_sequence'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewassignment',
            name='withdrawn',
            field=models.BooleanField(default=False),
        ),
    ]
