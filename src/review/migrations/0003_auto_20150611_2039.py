# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0002_auto_20150611_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formelement',
            name='choices',
            field=models.CharField(help_text=b'Seperate choices with the bar | character.', max_length=500, null=True, blank=True),
        ),
    ]
