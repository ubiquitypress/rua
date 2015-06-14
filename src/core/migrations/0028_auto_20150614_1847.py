# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_reviewassignment_results'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewassignment',
            name='results',
            field=models.ForeignKey(blank=True, to='review.FormResult', null=True),
        ),
    ]
