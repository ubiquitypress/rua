# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0006_auto_20160120_1640'),
        ('submission', '0025_proposalreview_requestor'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposalreview',
            name='review_form',
            field=models.ForeignKey(blank=True, to='review.Form', null=True),
        ),
    ]
