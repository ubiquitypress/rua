# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_role_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='roles',
            field=models.ManyToManyField(to='core.Role'),
        ),
    ]
