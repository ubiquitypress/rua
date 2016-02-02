# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0003_proposal_requestor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='data',
            field=models.TextField(null=True, blank=True),
        ),
    ]
