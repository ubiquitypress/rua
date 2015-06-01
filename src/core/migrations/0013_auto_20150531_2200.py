# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20150531_2153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileversion',
            name='date_uploaded',
            field=models.DateTimeField(),
        ),
    ]
