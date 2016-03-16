# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0013_proposal_book_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposalreview',
            name='withdrawn',
            field=models.BooleanField(default=False),
        ),
    ]
