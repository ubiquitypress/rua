# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_reviewassignment_recommendation'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewassignment',
            name='declined',
            field=models.DateField(null=True, blank=True),
        ),
    ]
