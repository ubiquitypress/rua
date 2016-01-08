# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0074_remove_profile_primary_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='reset_code',
            field=models.TextField(null=True, blank=True),
        ),
    ]
