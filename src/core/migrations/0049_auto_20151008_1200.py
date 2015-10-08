# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0048_auto_20151008_1155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='date_uploaded',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
