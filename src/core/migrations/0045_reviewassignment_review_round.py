# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0044_auto_20150708_1925'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewassignment',
            name='review_round',
            field=models.ForeignKey(blank=True, to='core.ReviewRound', null=True),
        ),
    ]
