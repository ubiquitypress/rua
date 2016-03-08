# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0093_profile_website'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='website',
            field=models.URLField(help_text=b"User's personal website. Remember to include http:// or https:// at the start.", max_length=2000, null=True, blank=True),
        ),
    ]
