# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0006_proposal_date_accepted'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposalreview',
            name='hide_details',
            field=models.BooleanField(default=False),
        ),
    ]
