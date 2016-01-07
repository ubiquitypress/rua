# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0003_proposal_requestor'),
        ('core', '0071_auto_20160106_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='emaillog',
            name='proposal',
            field=models.ForeignKey(blank=True, to='submission.Proposal', null=True),
        ),
        migrations.AlterField(
            model_name='emaillog',
            name='book',
            field=models.ForeignKey(blank=True, to='core.Book', null=True),
        ),
    ]
