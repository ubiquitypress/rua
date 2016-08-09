# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0133_auto_20160713_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='editorialreviewassignment',
            name='assigned',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='reviewassignment',
            name='assigned',
            field=models.DateField(auto_now_add=True),
        ),
    ]
