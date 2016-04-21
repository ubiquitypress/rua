# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0118_remove_contract_proposal'),
        ('submission', '0027_proposalreview_hide'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='contract',
            field=models.ForeignKey(related_name='contract_of_proposal', blank=True, to='core.Contract', null=True),
        ),
    ]
