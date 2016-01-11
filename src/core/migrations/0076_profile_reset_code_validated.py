# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0075_profile_reset_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='reset_code_validated',
            field=models.BooleanField(default=False),
        ),
    ]
