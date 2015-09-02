# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_auto_20150901_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposalformelement',
            name='name',
            field=models.CharField(max_length=1000),
        ),
    ]
