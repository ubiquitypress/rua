# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0028_proposal_contract'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposalreview',
            name='assigned',
            field=models.DateField(auto_now_add=True),
        ),
    ]
