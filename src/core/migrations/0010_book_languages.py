# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20150829_0123'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='languages',
            field=models.ManyToManyField(to='core.Language', null=True),
        ),
    ]
