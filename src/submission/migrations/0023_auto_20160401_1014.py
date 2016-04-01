# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0022_proposalnote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historyproposal',
            name='subtitle',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='subtitle',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
