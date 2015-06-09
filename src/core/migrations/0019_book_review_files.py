# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20150607_2141'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='review_files',
            field=models.ManyToManyField(related_name='review_files', null=True, to='core.File', blank=True),
        ),
    ]
