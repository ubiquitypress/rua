# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0006_auto_20160120_1640'),
        ('core', '0113_auto_20160415_0953'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewassignment',
            name='review_form',
            field=models.ForeignKey(blank=True, to='review.Form', null=True),
        ),
    ]
