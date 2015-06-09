# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20150609_2140'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewassignment',
            name='due',
            field=models.DateField(null=True, blank=True),
        ),
    ]
