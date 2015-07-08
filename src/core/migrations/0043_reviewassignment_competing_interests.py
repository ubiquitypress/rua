# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_book_competing_interests'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewassignment',
            name='competing_interests',
            field=models.TextField(null=True, blank=True),
        ),
    ]
