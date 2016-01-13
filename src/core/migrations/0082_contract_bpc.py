# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0081_auto_20160113_1206'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='bpc',
            field=models.DecimalField(default=Decimal('0.00'), max_digits=25, decimal_places=2),
        ),
    ]
