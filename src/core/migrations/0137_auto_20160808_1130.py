# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0136_book_first_run'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='institution',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
    ]
