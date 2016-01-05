# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0072_auto_20160105_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='proposal',
            field=models.ForeignKey(related_name='proposal_log', blank=True, to='submission.Proposal', null=True),
        ),
    ]
