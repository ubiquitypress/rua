# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0004_remove_formresult_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formresult',
            name='review_assignment',
        ),
    ]
