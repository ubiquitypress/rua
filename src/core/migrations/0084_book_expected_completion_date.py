# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0083_book_production_editors'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='expected_completion_date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
