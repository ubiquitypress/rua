# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0003_auto_20151022_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formelementsrelationship',
            name='element_class',
            field=models.CharField(blank=True, max_length=20, null=True, choices=[(b'col-md-4', b'third'), (b'col-md-6', b'half'), (b'col-md-12', b'full')]),
        ),
    ]
