# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0132_auto_20160713_1015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='publisher_location',
            field=models.CharField(help_text=b'Location of publisher imprint.', max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='series',
            field=models.ForeignKey(blank=True, to='core.Series', help_text=b'If you are submitting this work to an existing Series please select it.', null=True),
        ),
    ]
