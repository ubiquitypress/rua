# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0129_auto_20160627_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='name',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
    ]
