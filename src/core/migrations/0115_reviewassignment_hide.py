# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0114_reviewassignment_review_form'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewassignment',
            name='hide',
            field=models.BooleanField(default=False),
        ),
    ]
