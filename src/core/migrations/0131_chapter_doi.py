# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0130_chapter_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='doi',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
    ]
