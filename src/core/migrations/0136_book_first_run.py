# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0135_book_production_files'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='first_run',
            field=models.BooleanField(default=True),
        ),
    ]
