# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0078_auto_20160112_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='date_last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='note',
            name='date_submitted',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
