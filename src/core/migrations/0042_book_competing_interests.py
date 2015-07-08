# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0041_auto_20150708_1853'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='competing_interests',
            field=models.TextField(help_text=b"If any of the authors or editors have any competing interests please add them here. EG. 'This study was paid for by corp xyz.'", null=True, blank=True),
        ),
    ]
