# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0027_proposalreview_hide'),
        ('core', '0115_reviewassignment_hide'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='book',
            field=models.ForeignKey(related_name='book_contract', blank=True, to='core.Book', null=True),
        ),
        migrations.AddField(
            model_name='contract',
            name='proposal',
            field=models.ForeignKey(related_name='proposal_contract', blank=True, to='submission.Proposal', null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='contract',
            field=models.ForeignKey(related_name='contract_of_book', blank=True, to='core.Contract', null=True),
        ),
    ]
