# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0026_proposalreview_review_form'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposalreview',
            name='hide',
            field=models.BooleanField(default=False),
        ),
    ]
