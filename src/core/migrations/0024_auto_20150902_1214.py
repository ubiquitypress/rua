# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_auto_20150902_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='publication_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='submission_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
