# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0134_auto_20160802_1012'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='production_files',
            field=models.ManyToManyField(related_name='production_files', null=True, to='core.File', blank=True),
        ),
    ]
