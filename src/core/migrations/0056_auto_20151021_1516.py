# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0055_auto_20151021_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='identifier',
            name='digital_format',
            field=models.ForeignKey(related_name='digital_format', blank=True, to='core.Format', null=True),
        ),
        migrations.AddField(
            model_name='identifier',
            name='physical_format',
            field=models.ForeignKey(blank=True, to='core.PhysicalFormat', null=True),
        ),
        migrations.AlterField(
            model_name='identifier',
            name='book',
            field=models.ForeignKey(blank=True, to='core.Book', null=True),
        ),
    ]
